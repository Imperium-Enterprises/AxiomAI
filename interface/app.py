import ctypes
import sys
import customtkinter as ctk
import os
import threading
import time


from core.controller import AxiomController
from core.brain import AxiomBrain


from interface.sidebar import Sidebar
from interface.theme import (
    apply_theme,
    AXIOM_COLORS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PANEL_RADIUS
)


class AxiomApp:


    def __init__(self):


        apply_theme()


        # =====================================
        # WINDOW
        # =====================================


        self.window = ctk.CTk()


        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Axiom.PersonalAI"
        )


        self.window.withdraw()


        self.window.title(
            "AXIOM // PERSONAL AI SYSTEM"
        )


        self.window.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )


        self.window.minsize(
            1200,
            750
        )


        self.window.configure(
            fg_color=AXIOM_COLORS["background"]
        )


        self.set_icon()


        self.controller = None

        self.brain = None

        self.current_page = None


        self.create_splash()


    # =====================================
    # ICON
    # =====================================


    def set_icon(self):


        try:


            if getattr(sys, "frozen", False):

                base_path = sys._MEIPASS

            else:

                base_path = os.path.dirname(
                    os.path.dirname(__file__)
                )


            icon_path = os.path.join(
                base_path,
                "assets",
                "axiom.ico"
            )


            if os.path.exists(icon_path):

                self.window.iconbitmap(
                    icon_path
                )


        except Exception as e:

            print(
                "Icon error:",
                e
            )


    # =====================================
    # SPLASH
    # =====================================


    def create_splash(self):


        self.splash = ctk.CTkToplevel()


        self.splash.geometry(
            "650x400"
        )


        self.splash.overrideredirect(
            True
        )


        self.splash.configure(
            fg_color=AXIOM_COLORS["background"]
        )


        self.splash.update_idletasks()


        x = (
            self.splash.winfo_screenwidth()
            -
            650
        ) // 2


        y = (
            self.splash.winfo_screenheight()
            -
            400
        ) // 2


        self.splash.geometry(
            f"650x400+{x}+{y}"
        )


        ctk.CTkLabel(

            self.splash,

            text="◈",

            font=(
                "Inter",
                80,
                "bold"
            ),

            text_color=AXIOM_COLORS["gold"]

        ).pack(
            pady=(35, 0)
        )


        ctk.CTkLabel(

            self.splash,

            text="AXIOM",

            font=(
                "Inter",
                42,
                "bold"
            ),

            text_color=AXIOM_COLORS["gold"]

        ).pack()


        ctk.CTkLabel(

            self.splash,

            text="PERSONAL AI COMMAND CENTER",

            font=(
                "Inter",
                14
            ),

            text_color=AXIOM_COLORS["muted"]

        ).pack()


        self.boot_text = ctk.CTkLabel(

            self.splash,

            text="Initializing systems...",

            font=(
                "Inter",
                15
            )

        )


        self.boot_text.pack(
            pady=35
        )


        self.progress = ctk.CTkProgressBar(

            self.splash,

            width=420,

            progress_color=AXIOM_COLORS["gold"]

        )


        self.progress.pack()


        self.progress.set(
            0
        )


        threading.Thread(

            target=self.boot_sequence,

            daemon=True

        ).start()


    def boot_sequence(self):


        steps = [

            "Loading neural core...",
            "Connecting memory vault...",
            "Preparing interface...",
            "Starting voice engine...",
            "AXIOM ONLINE."

        ]


        for i, step in enumerate(steps):


            time.sleep(0.7)


            self.splash.after(

                0,

                lambda s=step, p=(i + 1) / len(steps):

                self.update_boot(
                    s,
                    p
                )

            )


        time.sleep(1)


        self.splash.after(

            0,

            self.launch_main

        )


    def update_boot(
        self,
        text,
        progress
    ):


        self.boot_text.configure(
            text=text
        )


        self.progress.set(
            progress
        )


    # =====================================
    # LAUNCH MAIN
    # =====================================


    def launch_main(self):


        self.splash.destroy()


        self.window.deiconify()


        self.center_window()


        self.brain = AxiomBrain()


        self.create_layout()


        self.show_page(
            "Home"
        )


        self.window.after(

            700,

            self.start_controller

        )


    # =====================================
    # CENTER WINDOW
    # =====================================


    def center_window(self):


        self.window.update_idletasks()


        x = (

            self.window.winfo_screenwidth()

            -

            WINDOW_WIDTH

        ) // 2


        y = (

            self.window.winfo_screenheight()

            -

            WINDOW_HEIGHT

        ) // 2


        self.window.geometry(

            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"

        )


    # =====================================
    # MAIN UI LAYOUT
    # =====================================


    def create_layout(self):


        self.window.grid_columnconfigure(

            1,

            weight=1

        )


        self.window.grid_rowconfigure(

            1,

            weight=1

        )


        # =================================
        # TOP BAR
        # =================================


        self.topbar = ctk.CTkFrame(

            self.window,

            height=55,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=0

        )


        self.topbar.grid(

            row=0,

            column=0,

            columnspan=2,

            sticky="ew"

        )


        self.topbar.grid_columnconfigure(

            1,

            weight=1

        )


        ctk.CTkLabel(

            self.topbar,

            text="AXIOM // COMMAND CENTER",

            font=(

                "Inter",

                16,

                "bold"

            ),

            text_color=AXIOM_COLORS["gold"]

        ).grid(

            row=0,

            column=0,

            padx=25,

            pady=15

        )


        self.system_status = ctk.CTkLabel(

            self.topbar,

            text="● SYSTEM STARTING",

            font=(

                "Inter",

                13,

                "bold"

            ),

            text_color=AXIOM_COLORS["success"]

        )


        self.system_status.grid(

            row=0,

            column=2,

            padx=25

        )


        # =================================
        # SIDEBAR
        # =================================


        self.sidebar = Sidebar(

            self.window,

            self

        )


        self.sidebar.grid(

            row=1,

            column=0,

            sticky="ns"

        )


        # =================================
        # MAIN FRAME
        # =================================


        self.main_frame = ctk.CTkFrame(

            self.window,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=PANEL_RADIUS,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        self.main_frame.grid(

            row=1,

            column=1,

            sticky="nsew",

            padx=(25, 30),

            pady=25

        )


        # =================================
        # STATUS BAR
        # =================================


        self.statusbar = ctk.CTkFrame(

            self.window,

            height=35,

            fg_color=AXIOM_COLORS["sidebar"]

        )


        self.statusbar.grid(

            row=2,

            column=0,

            columnspan=2,

            sticky="ew"

        )


        ctk.CTkLabel(

            self.statusbar,

            text="AI READY   •   MEMORY ACTIVE   •   VOICE CONNECTED",

            font=(

                "Inter",

                12

            ),

            text_color=AXIOM_COLORS["muted"]

        ).pack(

            side="left",

            padx=25,

            pady=8

        )


    # =====================================
    # START CONTROLLER
    # =====================================


    def start_controller(self):


        try:


            self.controller = AxiomController(

                brain=self.brain

            )


            self.controller.start()


            self.system_status.configure(

                text="● AXIOM ONLINE",

                text_color=AXIOM_COLORS["success"]

            )


            print(
                "Axiom voice system online"
            )


        except Exception as e:


            self.system_status.configure(

                text="● SYSTEM ERROR",

                text_color=AXIOM_COLORS["danger"]

            )


            print(

                "Controller error:",

                e

            )


    # =====================================
    # PAGE LOADER
    # =====================================


    def show_page(
        self,
        page
    ):


        if self.current_page:


            self.current_page.destroy()


        try:


            if page == "Home":


                from interface.pages.home import HomePage


                self.current_page = HomePage(

                    self.main_frame

                )


            elif page == "Chat":


                from interface.pages.chat import ChatPage


                self.current_page = ChatPage(

                    self.main_frame,

                    self.brain

                )


            elif page == "Memory":


                from interface.pages.memory import MemoryPage


                self.current_page = MemoryPage(

                    self.main_frame

                )


            elif page == "Tasks":


                from interface.pages.tasks import TasksPage


                self.current_page = TasksPage(

                    self.main_frame

                )


            elif page == "Debug":


                from interface.pages.debug import DebugPage


                self.current_page = DebugPage(

                    self.main_frame

                )


            elif page == "Settings":


                from interface.pages.settings import SettingsPage


                self.current_page = SettingsPage(

                    self.main_frame,

                    self.brain

                )


            elif page == "Axiom Support":


                from interface.pages.axiom_support import AxiomSupportPage


                self.current_page = AxiomSupportPage(

                    self.main_frame,

                    self.brain

                )


            elif page == "Updates":


                from interface.pages.updates import UpdatesPage


                self.current_page = UpdatesPage(

                    self.main_frame,

                    self.brain

                )


            if self.current_page:


                self.current_page.pack(

                    fill="both",

                    expand=True,

                    padx=10,

                    pady=10

                )


        except Exception as e:

            import traceback

            traceback.print_exc()


    # =====================================
    # RUN
    # =====================================


    def run(self):


        self.window.protocol(

            "WM_DELETE_WINDOW",

            self.close

        )


        self.window.mainloop()


    # =====================================
    # CLOSE
    # =====================================


    def close(self):


        try:


            if self.controller:


                self.controller.shutdown()


        except Exception as e:


            print(

                "Shutdown error:",

                e

            )


        self.window.destroy()


if __name__ == "__main__":


    app = AxiomApp()


    app.run()