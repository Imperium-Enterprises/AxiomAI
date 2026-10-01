import customtkinter as ctk
import platform
import time


from core.status import AxiomStatus
from core.logger import logger


from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BODY_FONT,
    CARD_RADIUS
)



class DebugPage(ctk.CTkFrame):


    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )


        self.status = AxiomStatus()



        # =====================================
        # HEADER
        # =====================================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        header.pack(
            fill="x",
            padx=40,
            pady=(35,10)
        )


        ctk.CTkLabel(
            header,
            text="DIAGNOSTICS",
            font=TITLE_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            header,
            text="System monitoring and internal operations",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            pady=(5,0)
        )



        # =====================================
        # STATUS CARDS
        # =====================================

        cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        cards.pack(
            fill="x",
            padx=40,
            pady=25
        )


        for i in range(3):
            cards.grid_columnconfigure(
                i,
                weight=1
            )


        data = self.status.get_status()


        self.create_card(
            cards,
            0,
            "AI BRAIN",
            data.get("brain","UNKNOWN")
        )


        self.create_card(
            cards,
            1,
            "OLLAMA",
            data.get("ollama","UNKNOWN")
        )


        self.create_card(
            cards,
            2,
            "APPLICATIONS",
            data.get("apps","UNKNOWN")
        )



        # =====================================
        # SYSTEM INFO
        # =====================================

        system = ctk.CTkFrame(
            self,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        system.pack(
            fill="x",
            padx=40,
            pady=10
        )


        ctk.CTkLabel(
            system,
            text="SYSTEM INFORMATION",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(18,8)
        )


        info = (
            f"Operating System  : {platform.system()} {platform.release()}\n"
            f"Python Version    : {platform.python_version()}\n"
            f"Session Started   : {time.strftime('%H:%M:%S')}"
        )


        ctk.CTkLabel(
            system,
            text=info,
            font=BODY_FONT,
            justify="left",
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(0,20)
        )



        # =====================================
        # LOG TERMINAL
        # =====================================

        ctk.CTkLabel(
            self,
            text="LIVE SYSTEM LOGS",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w",
            padx=40,
            pady=(20,8)
        )


        terminal = ctk.CTkFrame(
            self,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        terminal.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0,30)
        )


        self.console = ctk.CTkTextbox(
            terminal,
            fg_color=AXIOM_COLORS["panel"],
            corner_radius=18,
            border_width=0,
            font=(
                "Consolas",
                13
            ),
            text_color=AXIOM_COLORS["success"]
        )


        self.console.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.refresh_logs()



    # =====================================
    # STATUS CARD
    # =====================================

    def create_card(
        self,
        parent,
        column,
        title,
        value
    ):


        card = ctk.CTkFrame(
            parent,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        card.grid(
            row=0,
            column=column,
            padx=12,
            sticky="nsew"
        )


        ctk.CTkLabel(
            card,
            text="●",
            font=(
                "Inter",
                22
            ),
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            pady=(18,5)
        )


        ctk.CTkLabel(
            card,
            text=title,
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack()


        ctk.CTkLabel(
            card,
            text=str(value),
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            pady=(8,18)
        )



    # =====================================
    # LOG LOOP
    # =====================================

    def refresh_logs(self):


        try:

            self.console.configure(
                state="normal"
            )


            self.console.delete(
                "1.0",
                "end"
            )


            for log in logger.get_logs():

                self.console.insert(
                    "end",
                    log + "\n"
                )


            self.console.configure(
                state="disabled"
            )


        except Exception as e:

            print(
                "Debug log error:",
                e
            )


        self.console.after(
            1000,
            self.refresh_logs
        )