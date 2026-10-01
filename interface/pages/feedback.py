import customtkinter as ctk


from core.feedback import FeedbackManager


from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BUTTON_FONT,
    BODY_FONT,
    CARD_RADIUS
)



class FeedbackPage(ctk.CTkFrame):


    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )


        self.manager = FeedbackManager()



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
            text="FEEDBACK PORTAL",
            font=TITLE_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            header,
            text="Help improve future Axiom releases",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            pady=(5,0)
        )



        # =====================================
        # FEEDBACK CARD
        # =====================================

        card = ctk.CTkFrame(
            self,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )


        card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=25
        )



        ctk.CTkLabel(
            card,
            text="MESSAGE",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20,10)
        )



        self.box = ctk.CTkTextbox(
            card,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            corner_radius=18,
            border_width=1,
            border_color=AXIOM_COLORS["border"],
            text_color=AXIOM_COLORS["text"]
        )


        self.box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0,25)
        )



        # =====================================
        # ACTION AREA
        # =====================================

        actions = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        actions.pack(
            pady=(0,10)
        )



        self.send_button = ctk.CTkButton(
            actions,
            text="SUBMIT FEEDBACK",
            width=280,
            height=55,
            corner_radius=16,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            text_color=AXIOM_COLORS["black"],
            hover_color=AXIOM_COLORS["gold_hover"],
            command=self.send
        )


        self.send_button.pack()



        self.status = ctk.CTkLabel(
            self,
            text="",
            font=BODY_FONT
        )


        self.status.pack(
            pady=(5,25)
        )




    # =====================================
    # SEND FEEDBACK
    # =====================================

    def send(self):


        text = self.box.get(
            "1.0",
            "end"
        ).strip()



        if not text:


            self.status.configure(
                text="⚠ Enter feedback before submitting.",
                text_color=AXIOM_COLORS["warning"]
            )


            return




        try:

            success = self.manager.send_feedback(
                text
            )


        except Exception as e:

            print(
                "Feedback error:",
                e
            )

            success = False




        if success:


            self.status.configure(
                text="✓ Feedback submitted successfully.",
                text_color=AXIOM_COLORS["success"]
            )


            self.box.delete(
                "1.0",
                "end"
            )


            self.send_button.configure(
                text="✓ SENT"
            )


            self.after(
                2000,
                lambda:
                self.send_button.configure(
                    text="SUBMIT FEEDBACK"
                )
            )



        else:


            self.status.configure(
                text="✕ Failed to send feedback.",
                text_color=AXIOM_COLORS["danger"]
            )