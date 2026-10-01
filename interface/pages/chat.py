import customtkinter as ctk
import threading

from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    BODY_FONT,
    BUTTON_FONT,
    CARD_RADIUS
)


class ChatPage(ctk.CTkFrame):


    def __init__(self, parent, brain):

        super().__init__(
            parent,
            fg_color="transparent"
        )


        self.brain = brain



        # =========================
        # HEADER
        # =========================


        header = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=CARD_RADIUS

        )


        header.pack(

            fill="x",

            padx=30,

            pady=25

        )



        ctk.CTkLabel(

            header,

            text="AXIOM CHAT",

            font=TITLE_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=20,

            pady=(15,0)

        )



        ctk.CTkLabel(

            header,

            text="Secure local AI communication channel",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["muted"]

        ).pack(

            anchor="w",

            padx=20,

            pady=(0,15)

        )





        # =========================
        # CHAT AREA
        # =========================


        self.chat_area = ctk.CTkScrollableFrame(

            self,

            fg_color=AXIOM_COLORS["card"],

            corner_radius=CARD_RADIUS

        )


        self.chat_area.pack(

            fill="both",

            expand=True,

            padx=30,

            pady=10

        )


        self.add_message(

            "AXIOM",

            "System online. Awaiting command."

        )





        # =========================
        # INPUT BAR
        # =========================


        input_box = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=CARD_RADIUS

        )


        input_box.pack(

            fill="x",

            padx=30,

            pady=(10,25)

        )



        self.entry = ctk.CTkEntry(

            input_box,

            height=55,

            corner_radius=15,

            font=BODY_FONT,

            placeholder_text="Enter command..."

        )


        self.entry.pack(

            side="left",

            fill="x",

            expand=True,

            padx=(15,10),

            pady=12

        )


        self.entry.bind(

            "<Return>",

            lambda e:self.send_message()

        )





        send = ctk.CTkButton(

            input_box,

            text="SEND",

            width=100,

            height=50,

            corner_radius=14,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["gold"],

            text_color=AXIOM_COLORS["black"],

            hover_color=AXIOM_COLORS["gold_hover"],

            command=self.send_message

        )


        send.pack(

            side="right",

            padx=15

        )

    # =========================
    # MESSAGE CREATOR
    # =========================


    def add_message(

        self,

        sender,

        message

    ):


        if sender == "AXIOM":


            bubble_color = AXIOM_COLORS["panel"]

            text_color = AXIOM_COLORS["gold"]

            side = "w"

            icon = "👑"


        else:


            bubble_color = AXIOM_COLORS["gold"]

            text_color = AXIOM_COLORS["black"]

            side = "e"

            icon = "👤"





        bubble = ctk.CTkFrame(

            self.chat_area,

            fg_color=bubble_color,

            corner_radius=CARD_RADIUS

        )


        bubble.pack(

            anchor=side,

            padx=20,

            pady=10

        )



        ctk.CTkLabel(

            bubble,

            text=f"{icon} {sender}",

            font=(

                "Inter",

                13,

                "bold"

            ),

            text_color=text_color

        ).pack(

            anchor="w",

            padx=15,

            pady=(10,0)

        )



        ctk.CTkLabel(

            bubble,

            text=message,

            font=BODY_FONT,

            text_color=text_color,

            wraplength=600,

            justify="left"

        ).pack(

            padx=15,

            pady=(5,15)

        )


        self.after(

            50,

            lambda:

            self.chat_area._parent_canvas.yview_moveto(1)

        )





    # =========================
    # SEND
    # =========================


    def send_message(self):


        text = self.entry.get().strip()



        if not text:

            return



        self.entry.delete(

            0,

            "end"

        )



        self.add_message(

            "USER",

            text

        )



        threading.Thread(

            target=self.get_response,

            args=(text,),

            daemon=True

        ).start()





    def get_response(self,text):


        try:


            response = self.brain.think(

                text

            )



            if response:


                self.after(

                    0,

                    lambda:

                    self.add_message(

                        "AXIOM",

                        response

                    )

                )



        except Exception as e:


            self.after(

                0,

                lambda:

                self.add_message(

                    "SYSTEM",

                    str(e)

                )

            )