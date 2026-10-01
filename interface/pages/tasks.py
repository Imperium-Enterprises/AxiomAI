from core.paths import REMINDERS_FILE
import customtkinter as ctk
import json
import os


from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BUTTON_FONT,
    BODY_FONT,
    CARD_RADIUS
)



class TasksPage(ctk.CTkFrame):


    def __init__(self, parent):

        super().__init__(

            parent,

            fg_color="transparent"

        )



        self.reminders_file = REMINDERS_FILE




        # =====================================
        # HEADER
        # =====================================


        header = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=CARD_RADIUS,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        header.pack(

            fill="x",

            padx=40,

            pady=(35,20)

        )



        ctk.CTkLabel(

            header,

            text="TASK CENTER",

            font=TITLE_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(20,5)

        )



        ctk.CTkLabel(

            header,

            text="Manage reminders and scheduled AI actions",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["text_secondary"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(0,10)

        )



        self.status = ctk.CTkLabel(

            header,

            text="● TASK SYSTEM READY",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["success"]

        )


        self.status.pack(

            anchor="w",

            padx=25,

            pady=(0,20)

        )







        # =====================================
        # TASK DATABASE PANEL
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

            pady=10

        )



        ctk.CTkLabel(

            panel,

            text="SCHEDULED OPERATIONS",

            font=HEADING_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(20,10)

        )





        self.task_box = ctk.CTkTextbox(

            panel,

            font=(

                "Consolas",

                13

            ),

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=18,

            border_width=1,

            border_color=AXIOM_COLORS["border"],

            text_color=AXIOM_COLORS["text"]

        )


        self.task_box.pack(

            fill="both",

            expand=True,

            padx=25,

            pady=(0,25)

        )







        # =====================================
        # ACTION BUTTON
        # =====================================


        refresh = ctk.CTkButton(

            self,

            text="↻  REFRESH TASKS",

            width=280,

            height=55,

            corner_radius=16,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["gold"],

            hover_color=AXIOM_COLORS["gold_hover"],

            text_color=AXIOM_COLORS["black"],

            command=self.load_tasks

        )


        refresh.pack(

            pady=(0,30)

        )



        self.load_tasks()






    # =====================================
    # LOAD TASKS
    # =====================================


    def load_tasks(self):


        self.task_box.configure(

            state="normal"

        )


        self.task_box.delete(

            "1.0",

            "end"

        )



        if not os.path.exists(self.reminders_file):


            self.status.configure(

                text="● NO TASK DATABASE",

                text_color=AXIOM_COLORS["warning"]

            )


            self.task_box.insert(

                "end",

                "NO REMINDERS FOUND.\n\n"

                "Axiom has no scheduled operations."

            )


            self.task_box.configure(

                state="disabled"

            )


            return






        try:


            with open(

                self.reminders_file,

                "r",

                encoding="utf-8"

            ) as file:


                reminders = json.load(file)





            if not reminders:


                self.status.configure(

                    text="● TASK QUEUE EMPTY",

                    text_color=AXIOM_COLORS["warning"]

                )


                self.task_box.insert(

                    "end",

                    "NO ACTIVE TASKS."

                )



            else:


                active = 0


                completed = 0



                self.task_box.insert(

                    "end",

                    "◆ ACTIVE REMINDERS\n"

                    + ("═" * 55)

                    + "\n\n"

                )



                for index, reminder in enumerate(reminders, 1):


                    finished = reminder.get(

                        "completed",

                        False

                    )



                    if finished:

                        completed += 1

                        icon = "✓"

                        state = "COMPLETED"

                    else:

                        active += 1

                        icon = "●"

                        state = "ACTIVE"





                    self.task_box.insert(

                        "end",

                        f"{icon} TASK #{index}\n"

                        f"{'─'*55}\n"

                        f"TIME\n"

                        f"{reminder.get('datetime','Unknown')}\n\n"

                        f"DESCRIPTION\n"

                        f"{reminder.get('text','No description')}\n\n"

                        f"STATUS\n"

                        f"{state}\n\n"

                    )





                self.status.configure(

                    text=(

                        f"● TASKS ONLINE  •  "

                        f"{active} ACTIVE  •  "

                        f"{completed} COMPLETE"

                    ),

                    text_color=AXIOM_COLORS["success"]

                )






            self.task_box.insert(

                "end",

                "\n\n◆ TIMER SYSTEM\n"

                + ("═" * 55)

                + "\n\n"

                "Live timers are managed by Axiom.\n"

                "Future timer history will appear here."

            )





        except Exception as e:


            self.status.configure(

                text="● TASK SYSTEM ERROR",

                text_color=AXIOM_COLORS["danger"]

            )


            self.task_box.insert(

                "end",

                f"TASK ERROR:\n\n{e}"

            )



        self.task_box.configure(

            state="disabled"

        )