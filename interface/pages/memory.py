from core.paths import MEMORY_FILE
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



class MemoryPage(ctk.CTkFrame):


    def __init__(self, parent):

        super().__init__(

            parent,

            fg_color="transparent"

        )



        self.memory_file = MEMORY_FILE



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

            pady=(35,15)

        )



        ctk.CTkLabel(

            header,

            text="MEMORY VAULT",

            font=TITLE_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(20,5)

        )



        ctk.CTkLabel(

            header,

            text="Stored conversations and AI knowledge database",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["text_secondary"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(0,10)

        )



        self.memory_status = ctk.CTkLabel(

            header,

            text="",

            font=BODY_FONT,

            text_color=AXIOM_COLORS["success"]

        )


        self.memory_status.pack(

            anchor="w",

            padx=25,

            pady=(0,20)

        )






        # =====================================
        # MEMORY TERMINAL
        # =====================================


        vault = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["card"],

            corner_radius=CARD_RADIUS,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        vault.pack(

            fill="both",

            expand=True,

            padx=40,

            pady=15

        )



        ctk.CTkLabel(

            vault,

            text="DATABASE CONTENT",

            font=HEADING_FONT,

            text_color=AXIOM_COLORS["gold"]

        ).pack(

            anchor="w",

            padx=25,

            pady=(20,10)

        )





        self.memory_box = ctk.CTkTextbox(

            vault,

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


        self.memory_box.pack(

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

            pady=(0,30)

        )





        refresh = ctk.CTkButton(

            actions,

            text="↻  REFRESH MEMORY",

            width=280,

            height=55,

            corner_radius=16,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["gold"],

            hover_color=AXIOM_COLORS["gold_hover"],

            text_color=AXIOM_COLORS["black"],

            command=self.load_memory

        )


        refresh.pack()





        self.load_memory()





    # =====================================
    # LOAD MEMORY
    # =====================================


    def load_memory(self):


        self.memory_box.configure(

            state="normal"

        )


        self.memory_box.delete(

            "1.0",

            "end"

        )



        if not os.path.exists(self.memory_file):


            self.memory_status.configure(

                text="● MEMORY DATABASE OFFLINE",

                text_color=AXIOM_COLORS["danger"]

            )


            self.memory_box.insert(

                "end",

                "NO MEMORY DATABASE FOUND.\n\n"

                "Axiom has not created a memory vault yet."

            )


            self.memory_box.configure(

                state="disabled"

            )


            return





        try:


            with open(

                self.memory_file,

                "r",

                encoding="utf-8"

            ) as file:


                data = json.load(file)





            if not data:


                self.memory_status.configure(

                    text="● MEMORY VAULT EMPTY",

                    text_color=AXIOM_COLORS["warning"]

                )


                self.memory_box.insert(

                    "end",

                    "AXIOM HAS NO STORED MEMORIES YET."

                )



            else:


                self.memory_status.configure(

                    text=f"● MEMORY ONLINE  •  {len(data)} ENTRIES",

                    text_color=AXIOM_COLORS["success"]

                )



                for key,value in data.items():


                    self.memory_box.insert(

                        "end",

                        "\n"

                        + "◆ "

                        + key.upper()

                        + "\n"

                        + ("─" * 55)

                        + "\n\n"

                    )



                    if isinstance(value,list):


                        for item in value:


                            if isinstance(item,dict):


                                role = item.get(

                                    "role",

                                    "UNKNOWN"

                                )


                                content = item.get(

                                    "content",

                                    ""

                                )


                                self.memory_box.insert(

                                    "end",

                                    f"[{role.upper()}]\n"

                                    f"{content}\n\n"

                                )


                            else:


                                self.memory_box.insert(

                                    "end",

                                    str(item)

                                    + "\n\n"

                                )


                    else:


                        self.memory_box.insert(

                            "end",

                            str(value)

                            +

                            "\n\n"

                        )





        except Exception as e:


            self.memory_status.configure(

                text="● MEMORY ERROR",

                text_color=AXIOM_COLORS["danger"]

            )


            self.memory_box.insert(

                "end",

                f"MEMORY ERROR:\n\n{e}"

            )



        self.memory_box.configure(

            state="disabled"

        )