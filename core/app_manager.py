from core.paths import APPS_FILE
import os
import json
import subprocess
import threading
import time
import winreg

import winshell
import psutil

try:
    import ollama
except ImportError:
    ollama = None

from core.logger import logger
from core.paths import APPS_FILE


class AppManager:


    def __init__(self):

        self.app_database = APPS_FILE

        self.apps = {}

        self.scan_lock = threading.Lock()

        self.load_apps()


        threading.Thread(
            target=self.delayed_scan,
            daemon=True
        ).start()



    # =========================
    # DATABASE SYSTEM
    # =========================


    def load_apps(self):

        if not os.path.exists(
            self.app_database
        ):

            self.apps = {}

            self.start_scan()

            return


        try:

            with open(
                self.app_database,
                "r"
            ) as file:

                self.apps = json.load(file)


            self.migrate_old_database()


        except Exception as e:

            print(
                "Database load error:",
                e
            )

            self.apps = {}



    def save_apps(self):

        try:

            with open(
                self.app_database,
                "w"
            ) as file:

                json.dump(
                    self.apps,
                    file,
                    indent=4
                )


        except Exception as e:

            print(
                "Database save error:",
                e
            )



    def migrate_old_database(self):

        changed = False


        for name, value in list(
            self.apps.items()
        ):

            if isinstance(
                value,
                str
            ):

                self.apps[name] = {

                    "name": name,

                    "type": self.detect_type(
                        value
                    ),

                    "target": value

                }

                changed = True



        if changed:

            self.save_apps()

            print(
                "Migrated old app database"
            )



    # =========================
    # APP FORMAT SYSTEM
    # =========================


    def create_app(
        self,
        name,
        app_type,
        target
    ):

        return {

            "name": name,

            "type": app_type,

            "target": target

        }



    def add_app(
        self,
        name,
        app_type,
        target
    ):

        clean = self.normalize_name(
            name
        )


        if not clean:

            return False


        if clean not in self.apps:


            self.apps[clean] = self.create_app(

                name,

                app_type,

                target

            )

            return True


        return False




    def detect_type(
        self,
        target
    ):


        if target.startswith(
            "shell:AppsFolder"
        ):

            return "store"


        if target.startswith(
            "steam://"
        ):

            return "steam"


        if target.endswith(
            ".exe"
        ):

            return "exe"


        return "unknown"



    # =========================
    # SCANNER CONTROL
    # =========================


    def start_scan(self):

        threading.Thread(
            target=self.update_apps,
            daemon=True
        ).start()



    def update_apps(self):

        if self.scan_lock.locked():

            return


        with self.scan_lock:


            logger.log(
                "Checking for new apps..."
            )


            scanners = [

                self.scan_exe_files,

                self.scan_shortcuts,

                self.scan_registry,

                self.scan_windows_apps,

                self.scan_other_drives,

                self.scan_steam,

                self.scan_epic,

                self.scan_xbox,

                self.scan_battlenet

            ]


            added = 0


            for scanner in scanners:


                try:

                    results = scanner()


                    for app in results:


                        if self.add_app(

                            app["name"],

                            app["type"],

                            app["target"]

                        ):

                            added += 1


                except Exception as e:

                    print(
                        "Scanner error:",
                        e
                    )



            if added:


                self.save_apps()

                print(
                    f"Added {added} apps"
                )


            else:

                print(
                    "No new apps found"
                )



    # =========================
    # BACKGROUND SCAN
    # =========================


    def delayed_scan(self):

        time.sleep(30)

        self.background_scan()



    def background_scan(self):

        while True:

            try:

                self.update_apps()


            except Exception as e:

                print(
                    "Background scan error:",
                    e
                )


            time.sleep(
                3600
            )



    # =========================
    # HELPERS
    # =========================


    def normalize_name(
        self,
        name
    ):

        return (

            name

            .lower()

            .replace(
                ".exe",
                ""
            )

            .replace(
                "_",
                " "
            )

            .strip()

        )
    
        # =========================
    # SHORTCUT SCANNER
    # =========================

    def scan_shortcuts(self):

        found = []

        locations = [

            os.path.expanduser(
                r"~\Desktop"
            ),

            os.path.expandvars(
                r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
            ),

            os.path.expandvars(
                r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
            )

        ]


        for location in locations:

            if not os.path.exists(location):
                continue


            for root, dirs, files in os.walk(location):

                for file in files:

                    if not file.lower().endswith(".lnk"):
                        continue


                    shortcut = os.path.join(
                        root,
                        file
                    )


                    try:

                        target = winshell.shortcut(
                            shortcut
                        ).path


                        if target and target.lower().endswith(".exe"):

                            found.append({

                                "name": file,

                                "type": "exe",

                                "target": target

                            })


                    except Exception:

                        pass


        return found



    # =========================
    # REGISTRY SCANNER
    # =========================

    def scan_registry(self):

        found = []


        keys = [

            winreg.HKEY_LOCAL_MACHINE,

            winreg.HKEY_CURRENT_USER

        ]


        paths = [

            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",

            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"

        ]


        for key in keys:

            for path in paths:

                try:

                    registry = winreg.OpenKey(
                        key,
                        path
                    )


                    count = winreg.QueryInfoKey(
                        registry
                    )[0]


                    for i in range(count):

                        try:

                            sub = winreg.EnumKey(
                                registry,
                                i
                            )


                            app = winreg.OpenKey(
                                registry,
                                sub
                            )


                            name = winreg.QueryValueEx(
                                app,
                                "DisplayName"
                            )[0]


                            try:

                                location = winreg.QueryValueEx(
                                    app,
                                    "InstallLocation"
                                )[0]


                            except:

                                continue


                            if location:

                                found.append({

                                    "name": name,

                                    "type": "unknown",

                                    "target": location

                                })


                        except:

                            pass


                except:

                    pass


        return found



    # =========================
    # MICROSOFT STORE SCANNER
    # =========================

    def scan_windows_apps(self):

        found = []


        try:

            result = subprocess.check_output(

                [

                    "powershell",

                    "-Command",

                    "Get-StartApps | ConvertTo-Json"

                ],

                text=True

            )


            apps = json.loads(
                result
            )


            if isinstance(apps, dict):

                apps = [apps]


            for app in apps:

                name = app.get(
                    "Name"
                )

                app_id = app.get(
                    "AppID"
                )


                if name and app_id:

                    found.append({

                        "name": name,

                        "type": "store",

                        "target":

                            "shell:AppsFolder\\"

                            +

                            app_id

                    })


        except Exception as e:

            print(
                "Store scan error:",
                e
            )


        return found
    
        # =========================
    # OTHER DRIVE SCANNER
    # =========================

    def scan_other_drives(self):

        found = []


        for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":

            drive = letter + ":\\"

            if not os.path.exists(drive):
                continue


            try:

                for root, dirs, files in os.walk(drive):

                    dirs[:] = [

                        d for d in dirs

                        if d.lower() not in [

                            "windows",

                            "$recycle.bin",

                            "system volume information",

                            "node_modules",

                            "__pycache__"

                        ]

                    ]


                    for file in files:

                        if file.lower().endswith(".exe"):

                            found.append({

                                "name": file,

                                "type": "exe",

                                "target": os.path.join(
                                    root,
                                    file
                                )

                            })


            except PermissionError:

                continue


        return found



    # =========================
    # STEAM SCANNER
    # =========================

    def scan_steam(self):

        found = []

        steam_locations = [

            r"C:\Program Files (x86)\Steam",

            r"C:\Program Files\Steam"

        ]


        libraries = []


        for steam_path in steam_locations:

            if not os.path.exists(steam_path):
                continue


            libraries.append(
                steam_path
            )


            library_file = os.path.join(

                steam_path,

                "steamapps",

                "libraryfolders.vdf"

            )


            if os.path.exists(library_file):

                try:

                    with open(

                        library_file,

                        "r",

                        encoding="utf-8",

                        errors="ignore"

                    ) as file:

                        data = file.read()



                    for line in data.splitlines():

                        if '"path"' in line:

                            path = line.split('"')[3]

                            libraries.append(
                                path
                            )


                except Exception as e:

                    print(
                        "Steam library error:",
                        e
                    )



        for library in libraries:

            common = os.path.join(

                library,

                "steamapps",

                "common"

            )


            if not os.path.exists(common):
                continue


            try:

                for game in os.listdir(common):

                    game_path = os.path.join(

                        common,

                        game

                    )


                    if os.path.isdir(game_path):

                        found.append({

                            "name": game,

                            "type": "steam",

                            "target": game

                        })


            except:

                pass


        return found
    

        # =========================
    # EXE SCANNER
    # =========================

    def scan_exe_files(self):

        found = []


        locations = [

            r"C:\Program Files",

            r"C:\Program Files (x86)",

            os.path.expanduser(
                r"~\AppData\Local"
            ),

            os.path.expanduser(
                r"~\AppData\Roaming"
            )

        ]


        for location in locations:

            if not os.path.exists(location):

                continue


            try:

                for root, dirs, files in os.walk(location):

                    dirs[:] = [

                        d for d in dirs

                        if d.lower() not in [

                            "windows",

                            "$recycle.bin",

                            "system volume information",

                            "node_modules",

                            "__pycache__"

                        ]

                    ]


                    for file in files:

                        if file.lower().endswith(".exe"):

                            found.append({

                                "name": file,

                                "type": "exe",

                                "target": os.path.join(

                                    root,

                                    file

                                )

                            })


            except Exception as e:

                print(
                    "EXE scan error:",
                    e
                )


        return found



    # =========================
    # EPIC GAMES SCANNER
    # =========================

    def scan_epic(self):

        found = []


        locations = [

            r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests",

            r"C:\ProgramData\Epic\UnrealEngineLauncher"

        ]


        for location in locations:

            if not os.path.exists(location):
                continue


            try:

                for root, dirs, files in os.walk(location):

                    for file in files:

                        if not file.endswith(".item"):
                            continue


                        path = os.path.join(

                            root,

                            file

                        )


                        with open(

                            path,

                            "r",

                            encoding="utf-8",

                            errors="ignore"

                        ) as f:

                            data = json.load(f)



                        name = data.get(
                            "DisplayName"
                        )


                        app = data.get(
                            "AppName"
                        )


                        if name and app:

                            found.append({

                                "name": name,

                                "type": "epic",

                                "target": app

                            })


            except Exception as e:

                print(
                    "Epic scan error:",
                    e
                )


        return found



    # =========================
    # XBOX SCANNER
    # =========================

    def scan_xbox(self):

        found = []


        try:

            result = subprocess.check_output(

                [

                    "powershell",

                    "-Command",

                    "Get-StartApps | ConvertTo-Json"

                ],

                text=True

            )


            apps = json.loads(
                result
            )


            if isinstance(apps, dict):

                apps = [apps]



            for app in apps:

                name = app.get(
                    "Name"
                )


                appid = app.get(
                    "AppID"
                )


                if (

                    name

                    and

                    appid

                    and

                    (

                        "xbox" in name.lower()

                        or

                        "game" in name.lower()

                    )

                ):


                    found.append({

                        "name": name,

                        "type": "store",

                        "target":

                            "shell:AppsFolder\\"

                            +

                            appid

                    })


        except:

            pass


        return found
    
        # =========================
    # BATTLE.NET SCANNER
    # =========================

    def scan_battlenet(self):

        found = []


        locations = [

            r"C:\Program Files (x86)\Battle.net",

            r"C:\Program Files\Battle.net"

        ]


        for location in locations:

            if os.path.exists(location):

                found.append({

                    "name": "Battle.net",

                    "type": "exe",

                    "target": os.path.join(

                        location,

                        "Battle.net Launcher.exe"

                    )

                })


        return found



    # =========================
    # FIND APPLICATION
    # =========================

    def find_app(
        self,
        name
    ):

        name = self.normalize_name(
            name
        )


        if name in self.apps:

            return self.apps[name]


        for app, data in self.apps.items():


            if name in app:

                return data



            if isinstance(
                data,
                dict
            ):


                real_name = self.normalize_name(

                    data.get(

                        "name",

                        ""

                    )

                )


                if name in real_name:

                    return data



        return self.ai_find_app(
            name
        )



    # =========================
    # AI MATCHER
    # =========================

    def ai_find_app(
        self,
        request
    ):

        if ollama is None:

            return None


        if not self.apps:

            return None



        names = list(
            self.apps.keys()
        )


        prompt = f"""

Match this request to an installed app.

User:
{request}


Apps:
{names}


Rules:
Return only the app name.
No explanation.
If none match return NONE.

"""

        try:

            result = ollama.chat(

                model="llama3.2:3b",

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                options={

                    "temperature": 0

                }

            )


            answer = (

                result["message"]["content"]

                .lower()

                .strip()

            )


            if answer == "none":

                return None


            return self.apps.get(
                answer
            )


        except:

            return None



    # =========================
    # UNIVERSAL APP LAUNCHER
    # =========================

    def open_app(
        self,
        name
    ):

        app = self.find_app(
            name
        )


        if not app:

            return (
                f"I couldn't find {name}"
            )


        if isinstance(
            app,
            str
        ):

            app = {

                "type": self.detect_type(app),

                "target": app

            }


        app_type = app.get(
            "type",
            "unknown"
        )


        target = app.get(
            "target"
        )


        try:


            if app_type == "steam":

                subprocess.Popen(

                    [

                        "explorer.exe",

                        f"steam://rungameid/{self.get_steam_id(target)}"

                    ]

                )


            elif app_type == "epic":

                subprocess.Popen(

                    [

                        "explorer.exe",

                        f"com.epicgames.launcher://apps/{target}"

                    ]

                )


            elif app_type == "store":

                subprocess.Popen(

                    [

                        "explorer.exe",

                        target

                    ]

                )


            else:


                if not os.path.exists(target):

                    return (
                        "The app file no longer exists."
                    )


                subprocess.Popen(

                    [target],

                    cwd=os.path.dirname(
                        target
                    )

                )


            return (
                f"Opening {name}"
            )


        except Exception as e:

            print(
                "Open app error:",
                e
            )

            return (
                "I couldn't open it"
            )



    # =========================
    # STEAM ID LOOKUP
    # =========================

    def get_steam_id(
        self,
        game
    ):

        known_games = {

            "Geometry Dash":

            "322170"

        }


        return known_games.get(

            game,

            game

        )



    # =========================
    # CLOSE APPLICATION
    # =========================

    def close_app(
        self,
        name
    ):

        name = self.normalize_name(
            name
        )


        protected = [

            "explorer",

            "windows",

            "system",

            "axiom",

            "python"

        ]


        if name in protected:

            return (

                "I won't close that because it could affect the system."

            )


        closed = 0


        for process in psutil.process_iter(

            ["name"]

        ):

            try:

                process_name = process.info["name"]


                if not process_name:

                    continue


                clean = self.normalize_name(

                    process_name

                )


                if name in clean:

                    process.terminate()

                    closed += 1


            except:

                pass



        if closed:

            return (
                f"Closed {name}."
            )


        return (
            f"I couldn't find {name} running."
        )