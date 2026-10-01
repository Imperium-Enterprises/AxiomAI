import threading
import customtkinter as ctk

from core.state import state
from core.status import AxiomStatus

from interface.theme import (
    AXIOM_COLORS,
    HERO_TITLE,
    HEADING_FONT,
    BODY_FONT,
    BUTTON_FONT,
    CARD_RADIUS
)



class HomePage(ctk.CTkFrame):


    def __init__(self,parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )


        self.status = AxiomStatus()



        # =====================================
        # HERO
        # =====================================

        hero = ctk.CTkFrame(
            self,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=28,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        hero.pack(
            fill="x",
            padx=40,
            pady=35
        )



        ctk.CTkLabel(
            hero,
            text="AXIOM",
            font=HERO_TITLE,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            pady=(35,0)
        )


        ctk.CTkLabel(
            hero,
            text="PERSONAL AI COMMAND CENTER",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack()



        self.status_label = ctk.CTkLabel(
            hero,
            text="",
            font=HEADING_FONT
        )


        self.status_label.pack(
            pady=20
        )



        self.power_button = ctk.CTkButton(
            hero,
            text="",
            width=360,
            height=65,
            corner_radius=16,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            text_color=AXIOM_COLORS["black"],
            hover_color=AXIOM_COLORS["gold_hover"],
            command=self.toggle_power
        )


        self.power_button.pack(
            pady=(0,35)
        )


        self.update_power_display()



        # =====================================
        # STATUS CARDS
        # =====================================

        ctk.CTkLabel(
            self,
            text="SYSTEM STATUS",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w",
            padx=40,
            pady=(10,10)
        )



        cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        cards.pack(
            fill="x",
            padx=40
        )


        for i in range(3):

            cards.grid_columnconfigure(
                i,
                weight=1
            )



        self.ai = self.create_card(
            cards,
            0,
            "AI CORE",
            "ONLINE"
        )


        self.memory = self.create_card(
            cards,
            1,
            "MEMORY",
            "ACTIVE"
        )


        self.apps = self.create_card(
            cards,
            2,
            "APPLICATIONS",
            "READY"
        )


        self.load_status()



        # =====================================
        # QUICK ACCESS
        # =====================================

        ctk.CTkLabel(
            self,
            text="QUICK ACCESS",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w",
            padx=40,
            pady=(35,10)
        )



        quick = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        quick.pack()



        for text in [
            "CHAT",
            "MEMORY",
            "SETTINGS"
        ]:

            ctk.CTkButton(
                quick,
                text=text,
                width=210,
                height=60,
                corner_radius=CARD_RADIUS,
                font=BUTTON_FONT,
                fg_color=AXIOM_COLORS["card"],
                hover_color=AXIOM_COLORS["card_hover"]
            ).pack(
                side="left",
                padx=10
            )




    # =====================================
    # CARD
    # =====================================

    def create_card(
        self,
        parent,
        column,
        title,
        value
    ):


        frame = ctk.CTkFrame(
            parent,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        frame.grid(
            row=0,
            column=column,
            padx=12,
            sticky="nsew"
        )


        ctk.CTkLabel(
            frame,
            text="●",
            font=("Inter",28),
            text_color=AXIOM_COLORS["success"]
        ).pack(
            pady=(20,0)
        )


        ctk.CTkLabel(
            frame,
            text=title,
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack()


        label = ctk.CTkLabel(
            frame,
            text=value,
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        )


        label.pack(
            pady=(0,20)
        )


        return label



    # =====================================
    # STATUS
    # =====================================

    def load_status(self):

        threading.Thread(
            target=self.get_status,
            daemon=True
        ).start()



    def get_status(self):

        try:

            data = self.status.get_status()

            self.after(
                0,
                lambda:self.update_cards(data)
            )


        except Exception:

            pass




    def update_cards(self,data):


        self.ai.configure(
            text=data.get(
                "ollama",
                "UNKNOWN"
            )
        )


        self.memory.configure(
            text=data.get(
                "memory",
                "UNKNOWN"
            )
        )


        self.apps.configure(
            text=data.get(
                "apps",
                "UNKNOWN"
            )
        )




    # =====================================
    # POWER
    # =====================================

    def toggle_power(self):

        if state.is_suspended():

            state.resume()

        else:

            state.suspend()


        self.update_power_display()




    def update_power_display(self):


        if state.is_suspended():


            self.status_label.configure(
                text="● AXIOM SLEEPING",
                text_color=AXIOM_COLORS["danger"]
            )


            self.power_button.configure(
                text="WAKE SYSTEM"
            )


        else:


            self.status_label.configure(
                text="● AXIOM ONLINE",
                text_color=AXIOM_COLORS["success"]
            )


            self.power_button.configure(
                text="SUSPEND SYSTEM"
            )