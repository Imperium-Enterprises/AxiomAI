import glob
import tempfile
from core.state import state
from difflib import get_close_matches
import re
import os
import json
import time
import asyncio
import threading
import queue
import requests
import webbrowser

import pygame
import edge_tts

from ddgs import DDGS

try:
    import ollama
except ImportError:
    ollama = None


import dateparser


from core.settings_manager import SettingsManager
from core.logger import logger
from core.app_manager import AppManager
from core.reminder_manager import ReminderManager
from core.timer_manager import TimerManager
from core.memory_manager import MemoryManager
from core.update_manager import UpdateManager



class AxiomBrain:


    def __init__(self):


        # =========================
        # AUDIO ENGINE
        # =========================

        try:

            pygame.mixer.init()

    

        except Exception as e:

            print(
                "Audio initialization failed:",
                e
            )





        self.speech_queue = queue.Queue()


        self.wake_words = [
            "terminal start",
        ]
        self.stop_speech_event = threading.Event()

        self.interrupt_words = [
            "stop",
            "stop talking",
            "be quiet",
            "quiet",
            "cancel",
            "shut up"
        ]

        self.speaking_event = threading.Event()

        self.mic_lock = threading.Event()

        self.mic_cooldown = 0

        self.pending_action = None

    


        self.is_speaking = False

        self.suspended = False


        self.current_speech = ""

        self.last_spoken = ""

        self.pending_action = None


        self.speech_thread = threading.Thread(

            target=self._speech_worker,

            daemon=True

        )


        self.speech_thread.start()



        # =========================
        # CORE SYSTEMS
        # =========================


        self.app_manager = AppManager()



        self.timer_manager = TimerManager(

            self.speak

        )



        self.reminder_manager = ReminderManager(

            self.speak

        )



        self.settings = SettingsManager()


        self.config = self.settings.load()



        self.system = {

            "role": "system",

            "content": self.build_personality_prompt()

        }



        self.memory = MemoryManager()

        self.update_manager = UpdateManager()



        self.chat_log = (

            self.memory.recall(

                "chat_log"

            )

            or []

        )



        self.memory_summary = (

            self.memory.recall(

                "memory_summary"

            )

            or ""

        )



        self.last_active_time = time.time()



        self.folder_index = {


            "desktop":

                os.path.expanduser(

                    "~/Desktop"

                ),


            "downloads":

                os.path.expanduser(

                    "~/Downloads"

                ),


            "documents":

                os.path.expanduser(

                    "~/Documents"

                ),


            "music":

                os.path.expanduser(

                    "~/Music"

                ),


            "videos":

                os.path.expanduser(

                    "~/Videos"

                )

        }



        threading.Thread(

            target=self.reminder_loop,

            daemon=True

        ).start()



        # preload ollama

        threading.Thread(

            target=self.preload_model,

            daemon=True

        ).start()



    # =========================
    # APP CONFIRMATION SYSTEM
    # =========================

    def check_app_match(self, app_name):


        apps = self.app_manager.get_apps()


        app_names = list(apps.keys())


        if app_name in app_names:

            return app_name



        matches = get_close_matches(

            app_name,

            app_names,

            n=1,

            cutoff=0.65

        )


        if matches:

            return matches[0]


        return None




    # =========================
    # MODEL PRELOAD
    # =========================


    def preload_model(self):


        if ollama is None:

            return



        try:

            print(
                "Loading Axiom brain..."
            )


            ollama.chat(

                model="llama3.2:3b",

                messages=[

                    {

                        "role":"system",

                        "content":

                        "You are Axiom."

                    }

                ],

                options={

                    "num_predict":1

                }

            )


            print(

                "Axiom brain ready."

            )



        except Exception as e:


            print(

                "Model preload failed:",

                e

            )





    # =========================
    # PERSONALITY
    # =========================


    def build_personality_prompt(self):


        personality = self.config.get(
            "personality",
            "Sarcastic"
        )


        base = (

            "You are Axiom, a personal PC assistant.\n"
            "Created by Jaiden Henry.\n"
            "Never mention being an AI model.\n"
            "Keep answers short\n"
            "Answer naturally and intelligently.\n"
            "Adapt your response length to the question.\n"
            "Simple questions get short answers.\n"
            "Complex questions get detailed explanations.\n"
            "Give reasoning when useful.\n"
            "Do not avoid debates or discussions.\n"
            "Finish your thoughts completely. Do not end responses mid-explanation. If you need to shorten an answer, summarize the ending naturally instead of cutting yourself off.\n"

        )



        personalities = {

            "Sarcastic":

            (
                "You have a sarcastic, playful personality.\n"
                "Tease the user alot like a close friend.\n"
                "Use witty comments and playful remarks when appropriate.\n"
                "You can roast bad ideas or mistakes, but do not be genuinely rude.\n"
                "Do not sound like a corporate assistant.\n"
                "React with personality instead of only giving facts.\n"
                "Example style: 'Yeah, that was definitely the smartest move ever... totally.'\n"
                "Keep jokes short and still solve the user's problem.\n"
                "Keep answers short\n"
            ),



            "Professional":

            (
                "You are an expert technical assistant.\n"
                "Give intelligent, detailed answers when needed.\n"
                "Explain reasoning clearly.\n"
                "Keep simple answers short, but give detailed explanations when the situation requires it.\n"
                "Be capable of debates and comparing ideas logically.\n"
                "Challenge incorrect assumptions respectfully.\n"
                "Prioritize accuracy and depth over jokes.\n"
                "Do not oversimplify complex topics.\n"
            ),



            "Friendly":

            (
                "You are a friendly personal assistant.\n"
                "Keep answers short\n"
                "Be warm, conversational, and encouraging.\n"
                "Explain things clearly without sounding robotic.\n"
                "Make the user feel like they are talking to a helpful friend.\n"
                "Use casual language while staying useful.\n"
            )

        }



        return (

            base +

            personalities.get(

                personality,

                personalities["Sarcastic"]

            )

        )
    
    # =========================
    # TEXT TO SPEECH SYSTEM
    # =========================


    def suspend(self):

        self.suspended = True

        state.sleep()

        self.stop_speaking()


    def resume(self):

        self.suspended = False

        state.wake()


    def check_interrupt(self, text):

        text = text.lower().strip()


        for word in self.interrupt_words:

            if word in text:

                self.stop_speaking()

                return True


        return False


    def speak(self, text):


        if not self.config.get(

            "voice_enabled",

            True

        ):

            return



        if not text:

            return



        self.speech_queue.put(

            text

        )





    def stop_speaking(self):


        try:


            self.stop_speech_event.set()


            pygame.mixer.music.stop()



            while not self.speech_queue.empty():

                try:

                    self.speech_queue.get_nowait()

                except:

                    break



            self.is_speaking = False

            self.speaking_event.clear()

            self.mic_lock.clear()



            logger.log(

                "Speech interrupted"

            )



        except Exception as e:


            print(

                "Stop speaking error:",

                e

            )





    def _speech_worker(self):

        while True:

            text = self.speech_queue.get()

            self.stop_speech_event.clear()

            self.current_speech = text
            self.last_spoken = text.lower()

            self.is_speaking = True

            filename = None

            try:

                # =====================================
                # CREATE TTS FILE IN USER TEMP DIRECTORY
                # =====================================

                fd, filename = tempfile.mkstemp(
                    prefix="axiom_voice_",
                    suffix=".mp3"
                )

                os.close(fd)

                # Clean TTS formatting but keep natural speech pauses

                text = text.replace(
                    "\n",
                    " "
                )

                text = text.replace(
                    "...",
                    ","
                )

                text = text.replace(
                    "—",
                    ","
                )

                text = text.replace(
                    "-",
                    " "
                )

                text = " ".join(
                    text.split()
                )

                logger.log(
                    f"Axiom speaking: {text}"
                )

                # =====================================
                # EDGE TTS
                # =====================================

                async def generate():

                    await edge_tts.Communicate(
                        text,
                        "en-US-GuyNeural",
                        rate="-5%",
                        pitch="+2Hz"
                    ).save(
                        filename
                    )

                asyncio.run(
                    generate()
                )

                # =====================================
                # INTERRUPT CHECK
                # =====================================

                if self.stop_speech_event.is_set():

                    continue

                # =====================================
                # PLAY AUDIO
                # =====================================

                pygame.mixer.music.load(
                    filename
                )

                self.speaking_event.set()

                self.mic_lock.set()

                pygame.mixer.music.set_volume(
                    0.25
                )

                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():

                    if self.stop_speech_event.is_set():

                        pygame.mixer.music.stop()

                        break

                    time.sleep(0.05)

            except Exception as e:

                print(
                    "TTS error:",
                    e
                )

            finally:

                self.speaking_event.clear()

                time.sleep(0.15)

                self.mic_lock.clear()

                self.mic_cooldown = time.time()

                self.is_speaking = False

                self.current_speech = ""

                try:

                    pygame.mixer.music.stop()

                except:

                    pass

                # =====================================
                # DELETE TEMP AUDIO
                # =====================================

                if filename:

                    try:

                        if os.path.exists(filename):

                            os.remove(filename)

                    except Exception:

                        pass






    # =========================
    # APP CONTROL
    # =========================


    def open_app(self, app_name):


        return self.app_manager.open_app(

            app_name

        )




    def close_app(self, app_name):


        return self.app_manager.close_app(

            app_name

        )






    # =========================
    # REMINDERS
    # =========================


    def reminder_loop(self):


        while True:


            try:

                self.reminder_manager.check_reminders()

            except Exception as e:

                print(

                    "Reminder error:",

                    e

                )



            time.sleep(30)






    # =========================
    # INTERNET SEARCH
    # =========================


    def internet_search(self, query):


        try:


            print(

                "Searching:",

                query

            )



            with DDGS() as ddgs:


                results = list(

                    ddgs.text(

                        query,

                        max_results=3

                    )

                )



            if not results:

                return "No results found."



            context = "WEB RESULTS:\n"



            for result in results:


                context += (

                    result.get(

                        "title",

                        ""

                    )

                    +

                    "\n"

                    +

                    result.get(

                        "body",

                        ""

                    )[:300]

                    +

                    "\n\n"

                )



            return context



        except Exception as e:


            print(

                "Search error:",

                e

            )


            return "Search failed."






    # =========================
    # FOLDER SYSTEM
    # =========================


    def open_folder(self, folder_name):


        folder_name = folder_name.lower().strip()



        folders = self.folder_index.copy()



        folders["pictures"] = os.path.expanduser(

            "~/Pictures"

        )


        



        if folder_name not in folders:


            return (

                f"I don't know where {folder_name} is."

            )



        try:


            os.startfile(

                folders[folder_name]

            )


            return (

                f"Opening {folder_name}."

            )



        except:


            return (

                "I couldn't open that folder."

            )
        

    # =========================
    # FILE SEARCH
    # =========================


    def system_check(self, filename):


        filename = filename.lower().strip()


        start_time = time.time()



        drives = []



        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":


            drive = f"{letter}:\\"


            if os.path.exists(drive):

                drives.append(drive)



        matches = []



        for drive in drives:


            try:


                for root, dirs, files in os.walk(drive):


                    if time.time() - start_time > 20:


                        return (

                            "Search took too long. "

                            "Try a more specific name."

                        )



                    dirs[:] = [

                        d for d in dirs

                        if d.lower() not in [

                            "windows",

                            "$recycle.bin",

                            "system volume information",

                            "program files",

                            "program files (x86)"

                        ]

                    ]



                    for file in files:


                        if filename in file.lower():


                            matches.append(

                                os.path.join(

                                    root,

                                    file

                                )

                            )



                    if len(matches) >= 10:

                        break



            except:

                continue




        if matches:


            response = (

                f"Found {len(matches)} matches:\n"

            )


            for item in matches[:5]:


                response += item + "\n"



            return response




        return (

            f"I couldn't find {filename}."

        )







    # =========================
    # FOLDER FINDER
    # =========================


    def find_folder(self, folder_name):


        folder_name = folder_name.lower().strip()



        drives = []



        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":


            drive = f"{letter}:\\"


            if os.path.exists(drive):

                drives.append(drive)




        for drive in drives:


            try:


                for root, dirs, files in os.walk(drive):


                    dirs[:] = [

                        d for d in dirs

                        if d.lower() not in [

                            "windows",

                            "$recycle.bin",

                            "system volume information",

                            "__pycache__"

                        ]

                    ]



                    for folder in dirs:


                        if folder_name in folder.lower():


                            path = os.path.join(

                                root,

                                folder

                            )



                            try:


                                os.startfile(path)


                                return (

                                    f"Opening {folder}."

                                )


                            except:

                                pass



            except:

                continue




        return (

            f"I couldn't find {folder_name}."

        )






    # =========================
    # WEBSITE LOCATOR
    # =========================


    def locate_website(self, website):


        website = (

            website

            .lower()

            .strip()

        )



        website = (

            website

            .replace(

                "dot com",

                ""

            )

            .replace(

                ".com",

                ""

            )

            .strip()

        )



        domains = [

            ".com",

            ".org",

            ".net",

            ".io",

            ".gg"

        ]



        headers = {

            "User-Agent":

            "Mozilla/5.0"

        }



        for domain in domains:


            url = (

                "https://"

                +

                website.replace(

                    " ",

                    ""

                )

                +

                domain

            )



            try:


                response = requests.get(

                    url,

                    timeout=3,

                    headers=headers

                )



                if response.status_code < 400:


                    webbrowser.open(url)



                    return (

                        f"Opening {website}."

                    )


            except:

                pass




        webbrowser.open(

            "https://www.google.com/search?q="

            +

            website.replace(

                " ",

                "+"

            )

        )



        return (

            f"I searched for {website}."

        )







    # =========================
    # MEMORY SYSTEM
    # =========================


    def search_memory(self, query):


        query = query.lower()



        matches = [


            item

            for item in self.chat_log

            if query in item.get(

                "content",

                ""

            ).lower()


        ]



        if not matches:


            return (

                "I don't remember that."

            )



        return matches[-1]["content"]






    def compress_memory(self):


        if ollama is None:

            return



        if len(self.chat_log) < 50:

            return



        old = self.chat_log[:-20]


        recent = self.chat_log[-20:]



        try:


            result = ollama.chat(

                model="llama3.2:3b",

                messages=[

                    {

                        "role":"system",

                        "content":

                        "Summarize this conversation memory. Keep important facts."

                    },

                    {

                        "role":"user",

                        "content":str(old)

                    }

                ],

                options={

                    "temperature":0.3,

                    "num_predict":60

                }

            )



            summary = result["message"]["content"]



            self.memory_summary += (

                "\n" +

                summary

            )



            self.memory_summary = (

                self.memory_summary[-3000:]

            )



            self.chat_log = [

                {

                    "role":"system",

                    "content":

                    f"Memory: {self.memory_summary}"

                }

            ] + recent



        except Exception as e:


            print(

                "Compression failed:",

                e

            )





    def save_memory(self):


        if len(self.chat_log) > 100:


            self.chat_log = self.chat_log[-100:]



        self.memory.remember(

            "chat_log",

            self.chat_log

        )


        self.memory.remember(

            "memory_summary",

            self.memory_summary

        )



    # =========================
    # VOICE COMMAND CLEANER
    # =========================

    def clean_command(self, text):

        text = text.lower().strip()


        fixes = {

            # =========================
            # BROWSERS
            # =========================

            "google chrome": "chrome",
            "google chrome browser": "chrome",
            "chrome browser": "chrome",
            "chrom": "chrome",
            "crome": "chrome",
            "crohme": "chrome",
            "chromey": "chrome",
            "grome": "chrome",
            "chromee": "chrome",
            "chrome app": "chrome",


            "microsoft edge": "edge",
            "edge browser": "edge",
            "edg": "edge",
            "ej": "edge",
            "microsoft ed": "edge",


            "fire fox": "firefox",
            "fire fox browser": "firefox",
            "fire focks": "firefox",
            "fire vox": "firefox",
            "firefoxs": "firefox",



            # =========================
            # MUSIC
            # =========================

            "spot of five": "spotify",
            "spot if i": "spotify",
            "spot a fi": "spotify",
            "spot five": "spotify",
            "spotty five": "spotify",
            "spottyfy": "spotify",
            "spotifyy": "spotify",
            "sportify": "spotify",
            "sporty fi": "spotify",
            "spotify app": "spotify",


            "you tube music": "youtube music",
            "youtube": "youtube",
            "you tube": "youtube",
            "you too": "youtube",



            # =========================
            # GAMING
            # =========================

            "mine craft": "minecraft",
            "mind craft": "minecraft",
            "my craft": "minecraft",
            "minecrafts": "minecraft",
            "minecraft app": "minecraft",


            "steam": "steam",
            "steem": "steam",
            "steam app": "steam",


            "epic games": "epic games",
            "epic game": "epic games",
            "epic launcher": "epic games",
            "epic": "epic games",



            # =========================
            # COMMUNICATION
            # =========================

            "disc cord": "discord",
            "dis cord": "discord",
            "this cord": "discord",
            "discords": "discord",
            "discord app": "discord",


            "skype": "skype",
            "sky": "skype",


            "slack": "slack",
            "black": "slack",
   


            # =========================
            # DEVELOPMENT
            # =========================

            "visual studio code": "vscode",
            "visual studio": "vscode",
            "vs code": "vscode",
            "v s code": "vscode",
            "code studio": "vscode",
            "visual code": "vscode",


            "py charm": "pycharm",
            "pie charm": "pycharm",
            "py char": "pycharm",


            "terminal start": "terminal start",
            "terminal": "terminal start",
 



            # =========================
            # WINDOWS APPS
            # =========================

            "file explorer": "explorer",
            "file explore": "explorer",
            "files explorer": "explorer",
            "windows explorer": "explorer",


            "task manager": "task manager",
            "taskmanager": "task manager",
            "task manger": "task manager",

 
            "settings": "settings",
            "setting": "settings",
            "windows settings": "settings",
 


            # =========================
            # PRODUCTIVITY
            # =========================

            "microsoft word": "word",
            "micro soft word": "word",
            "word app": "word",


            "power point": "powerpoint",
            "power point app": "powerpoint",


            "one note": "onenote",
            "one note app": "onenote",


            "notepad plus plus": "notepad++",
            "note pad": "notepad",

        }


        for wrong, correct in fixes.items():

            if wrong in text:

                text = text.replace(
                    wrong,
                    correct
                )


        return text

    
    # =========================
    # MAIN THINK FUNCTION
    # =========================


    def think(self, text):

        lower = text.lower()


        # =========================
        # SPEECH INTERRUPT
        # =========================

        if self.check_interrupt(lower):

            return


        total_start = time.time()

        if self.suspended:
            return



        logger.log(

            f"Brain received: {text}"

        )



        self.last_active_time = time.time()
  



        

        print("AWAKE STATUS:", state.is_awake())
        print("HEARD:", lower)



        # =========================
        # COMMAND LOCK
        # =========================

        commands = [
            "open ",
            "close ",
            "run system check",
            "open folder",
            "remind me",
            "set a timer",
            "check for updates",
            "update my computer"
        ]


        if not state.is_awake() and not self.suspended:

            if any(lower.startswith(cmd) for cmd in commands):

                state.wake()
  

        # =========================
        # CONFIRMATION SYSTEM
        # =========================

        if self.pending_action:

            confirmations = [
                "yes",
                "yeah",
                "yep",
                "sure",
                "do it",
                "go ahead",
                "okay",
                "ok"
            ]

            declines = [
                "no",
                "nope",
                "cancel",
                "don't",
                "stop"
            ]


            if any(word in lower for word in confirmations):

                action = self.pending_action

                self.pending_action = None


                if action["type"] == "open":

                    self.speak(
                        f"Opening {action['name']}."
                    )

                    return self.open_app(
                        action["name"]
                    )


                if action["type"] == "close":

                    self.speak(
                        f"Closing {action['name']}."
                    )

                    return self.close_app(
                        action["name"]
                    )



            if any(word in lower for word in declines):

                self.pending_action = None

                self.speak(
                    "Cancelled."
                )

                return




        # =========================
        # UPDATES
        # =========================

        if "check for updates" in lower:

            self.speak(
                self.update_manager.check_updates()
            )

            return



        if "update my computer" in lower:

            self.speak(
                self.update_manager.install_updates()
            )

            return








        # =========================
        # REMINDERS
        # =========================


        if lower.startswith(

            "remind me"

        ):


            reminder = text[9:].strip()



            if " to " not in reminder:


                self.speak(

                    "Tell me what to remind you about."

                )

                return



            date_text, reminder_text = reminder.split(

                " to ",

                1

            )



            date = dateparser.parse(

                date_text

            )



            if date is None:


                self.speak(

                    "I couldn't understand that date."

                )

                return



            self.reminder_manager.add_reminder(

                date.strftime(

                    "%Y-%m-%d %H:%M"

                ),

                reminder_text

            )



            self.speak(

                "Reminder saved."

            )


            return





        # =========================
        # TIMER
        # =========================


        if lower.startswith(

            "set a timer for "

        ):


            timer = lower.replace(

                "set a timer for ",

                ""

            ).strip()



            try:


                amount = int(

                    timer.split()[0]

                )



                if "second" in timer:

                    seconds = amount


                elif "minute" in timer:

                    seconds = amount * 60


                elif "hour" in timer:

                    seconds = amount * 3600


                else:

                    raise Exception()



                self.timer_manager.set_timer(

                    seconds

                )



                self.speak(

                    f"Timer set for {timer}."

                )



            except:


                self.speak(

                    "I couldn't set that timer."

                )



            return





        # =========================
        # FILE SEARCH
        # =========================


        if lower.startswith(

            "run system check for "

        ):


            filename = text[len(

                "run system check for "

            ):].strip()



            self.speak(

                self.system_check(

                    filename

                )

            )


            return





        # =========================
        # FOLDERS
        # =========================


        if lower.startswith(
            "open folder "
        ):


            folder = lower.replace(
                "open folder ",
                ""
            ).strip()



            result = self.open_folder(
                folder
            )


            if "don't know" in result.lower():

                result = self.find_folder(
                    folder
                )



            self.speak(
                result
            )


            return





        # =========================
        # APP CONTROL
        # =========================


        if lower.startswith(
            "close "
        ):

            app = lower.replace(
                "close ",
                ""
            ).strip()


            result = self.close_app(
                app
            )


            if result.startswith(
                "Did you mean"
            ):

                self.pending_action = {
                    "type": "close",
                    "name": result.replace(
                        "Did you mean ",
                        ""
                    ).replace(
                        "?",
                        ""
                    )
                }
  

                self.speak(
                    result
                )

                return


            self.speak(
                result
            )   

            return





        if lower.startswith(
            "open "
        ):

            app = lower.replace(
                "open ",
                ""
           ).strip()


            result = self.open_app(
                app
            )


            if result.startswith(
                "Did you mean"
            ):

                self.pending_action = {
                    "type": "open",
                    "name": result.replace(
                        "Did you mean ",
                        ""
                    ).replace(
                        "?",
                        ""
                    )
                }

                self.speak(
                    result
                )

                return


            self.speak(
                result
            )

            return



        if ollama is None:

            self.speak(
                "My AI engine is not installed."
            )

            return
  

    


        # =========================
        # NORMAL CHAT
        # =========================


        self.chat_log.append(

            {

                "role":"user",

                "content":text

            }

        )



        try:

            self.compress_memory()

        except Exception as e:

            print(

                "Memory compression skipped:",

                e

            )





        internet_keywords = [

            "who is",

            "what is",

            "when",

            "where",

            "why",

            "latest",

            "news",

            "today",

            "weather",

            "search",

            "look up",

            "google"

        ]



        use_internet = any(

            word in lower

            for word in internet_keywords

        )





        if use_internet:


            search_results = self.internet_search(

                text

            )



            messages = [

                self.system,

                {

                    "role":"system",

                    "content":

                    "Use these search results only as information:\n\n"

                    + search_results

                }

            ] + self.chat_log[-6:]



        else:


            messages = [

                self.system

            ] + self.chat_log[-8:]





        start = time.time()



        try:


            response = ollama.chat(

                model="llama3.2:3b",

                stream=False,

                messages=messages,

                options={

                    "temperature":0.45,

                    "top_p":0.95,

                    "num_predict":180

                }

            )



        except Exception as e:


            print(

                "Ollama error:",

                e

            )


            self.speak(

                "My thinking system is unavailable."

            )


            return





        print(

            "OLLAMA TIME:",

            round(

                time.time()-start,

                2

            )

        )





        reply = response["message"]["content"]



        if not reply:


            reply = "Hmm."





        reply = reply.replace(

            "\n",

            " "

        )



        reply = re.sub(

            r"\s+",

            " ",

            reply

        )



        blocked = [

            "as an ai",

            "i am an ai",

            "i don't have consciousness",

            "here are some steps"

        ]



        for word in blocked:


            reply = reply.replace(

                word,

                ""

            )



        reply = reply.strip()





        words = reply.split()



        if len(words) > 80:


            reply = (

                " ".join(

                    words[:80]

                )

                +

                "."

            )





        self.chat_log.append(

            {

                "role":"assistant",

                "content":reply

            }

        )



        self.save_memory()



        self.speak(

            reply

        )



        print(

            "TOTAL BRAIN TIME:",

            round(

                time.time()-total_start,

                2

            ),

            "seconds"

        )



        return reply