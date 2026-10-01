import customtkinter as ctk
import threading


from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BUTTON_FONT,
    BODY_FONT,
    CARD_RADIUS
)



class UpdatesPage(ctk.CTkFrame):


    def __init__(self, parent, brain):


        super().__init__(

            parent,

            fg_color="transparent"

        )


        self.brain = brain



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

            text="UPDATE CENTER",

            font=TITLE_FONT,

            text_color=AXIOM_COLORS["text"]

        ).pack(

            anchor="w"

        )



        ctk.CTkLabel(

            header,

            text="System updates and maintenance controls",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["text_secondary"]

        ).pack(

            anchor="w",

            pady=(5,0)

        )





        # =====================================
        # UPDATE PANEL
        # =====================================


        panel = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["card"],

            corner_radius=CARD_RADIUS,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        panel.pack(

            fill="both",

            expand=True,

            padx=40,

            pady=25

        )



        ctk.CTkLabel(

            panel,

            text="SYSTEM UPDATE STATUS",

            font=HEADING_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(20,10)

        )





        self.status = ctk.CTkTextbox(

            panel,

            font=(

                "Consolas",

                13

            ),

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=18,

            border_width=1,

            border_color=AXIOM_COLORS["border"],

            text_color=AXIOM_COLORS["success"]

        )


        self.status.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0,20)

        )



        self.write_status(

            "AXIOM UPDATE SYSTEM ONLINE\n\n"

            "Ready for update scan."

        )





        # =====================================
        # ACTION BUTTONS
        # =====================================


        actions = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )


        actions.pack(

            pady=(0,35)

        )





        self.check_button = ctk.CTkButton(

            actions,

            text="CHECK FOR UPDATES",

            width=260,

            height=55,

            corner_radius=16,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["gold"],

            text_color=AXIOM_COLORS["black"],

            hover_color=AXIOM_COLORS["gold_hover"],

            command=self.check_updates

        )


        self.check_button.pack(

            side="left",

            padx=10

        )





        self.install_button = ctk.CTkButton(

            actions,

            text="INSTALL UPDATES",

            width=260,

            height=55,

            corner_radius=16,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["panel"],

            border_width=1,

            border_color=AXIOM_COLORS["border"],

            hover_color=AXIOM_COLORS["card_hover"],

            command=self.update_computer

        )


        self.install_button.pack(

            side="left",

            padx=10

        )





    # =====================================
    # WRITE STATUS
    # =====================================


    def write_status(self, text):


        self.status.configure(

            state="normal"

        )


        self.status.delete(

            "1.0",

            "end"

        )


        self.status.insert(

            "end",

            str(text)

        )


        self.status.configure(

            state="disabled"

        )





    # =====================================
    # CHECK UPDATES
    # =====================================


    def check_updates(self):


        self.check_button.configure(

            state="disabled",

            text="SCANNING..."

        )


        threading.Thread(

            target=self._check_updates_thread,

            daemon=True

        ).start()





    def _check_updates_thread(self):


        try:


            result = self.brain.update_manager.check_updates()


        except Exception as e:


            result = (

                "UPDATE SCAN FAILED\n\n"

                + str(e)

            )



        self.after(

            0,

            lambda:self.write_status(result)

        )


        self.after(

            0,

            lambda:self.check_button.configure(

                state="normal",

                text="CHECK FOR UPDATES"

            )

        )





    # =====================================
    # INSTALL UPDATES
    # =====================================


    def update_computer(self):


        self.install_button.configure(

            state="disabled",

            text="INSTALLING..."

        )


        threading.Thread(

            target=self._install_thread,

            daemon=True

        ).start()





    def _install_thread(self):


        try:


            result = self.brain.update_manager.install_updates()


        except Exception as e:


            result = (

                "UPDATE INSTALLATION FAILED\n\n"

                + str(e)

            )



        self.after(

            0,

            lambda:self.write_status(result)

        )


        self.after(

            0,

            lambda:self.install_button.configure(

                state="normal",

                text="INSTALL UPDATES"

            )

        )