import customtkinter as ctk
import psutil
import time


from interface.theme import (
    AXIOM_COLORS,
    STATUS_FONT
)



class TopBar(ctk.CTkFrame):


    def __init__(self, parent):


        super().__init__(

            parent,

            height=60,

            corner_radius=0,

            fg_color=AXIOM_COLORS["panel"]

        )


        self.pack_propagate(False)



        # ===============================
        # BRAND
        # ===============================


        self.logo = ctk.CTkLabel(

            self,

            text="◈  AXIOM",

            font=(

                "Inter",

                19,

                "bold"

            ),

            text_color=AXIOM_COLORS["gold"]

        )


        self.logo.pack(

            side="left",

            padx=28

        )





        # ===============================
        # SYSTEM INDICATOR
        # ===============================


        self.system = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["card"],

            corner_radius=14,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        self.system.pack(

            side="right",

            padx=20,

            pady=10

        )



        self.status = ctk.CTkLabel(

            self.system,

            text="",

            font=(

                "Inter",

                12,

                "bold"

            ),

            text_color=AXIOM_COLORS["text_secondary"]

        )


        self.status.pack(

            padx=18,

            pady=8

        )



        self.update_status()





    # ===============================
    # LIVE STATUS
    # ===============================


    def update_status(self):


        try:


            cpu = psutil.cpu_percent()

            ram = psutil.virtual_memory().percent


            clock = time.strftime(

                "%H:%M:%S"

            )



            self.status.configure(

                text=(

                    f"CPU {cpu}%   "

                    f"RAM {ram}%   "

                    "● VOICE READY   "

                    f"{clock}"

                )

            )


        except Exception:


            self.status.configure(

                text="● SYSTEM ONLINE"

            )



        self.after(

            1000,

            self.update_status

        )