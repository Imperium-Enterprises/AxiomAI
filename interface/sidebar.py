import customtkinter as ctk


from interface.theme import (
    AXIOM_COLORS,
    BUTTON_FONT,
    SIDEBAR_WIDTH,
    SIDEBAR_COLLAPSED,
    SIDEBAR_BUTTON_HEIGHT,
    SIDEBAR_BUTTON_RADIUS
)


class Sidebar(ctk.CTkFrame):


    def __init__(self, parent, app):


        super().__init__(

            parent,

            width=SIDEBAR_WIDTH,

            corner_radius=0,

            fg_color=AXIOM_COLORS["sidebar"]

        )


        self.app = app

        self.expanded = True

        self.active_button = None

        self.grid_propagate(False)


        # ===============================
        # LOGO
        # ===============================


        self.logo_frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )


        self.logo_frame.pack(

            fill="x",

            pady=(35, 20)

        )


        self.logo = ctk.CTkLabel(

            self.logo_frame,

            text="◈",

            font=(

                "Inter",

                46,

                "bold"

            ),

            text_color=AXIOM_COLORS["gold"]

        )


        self.logo.pack()


        self.title = ctk.CTkLabel(

            self.logo_frame,

            text="AXIOM",

            font=(

                "Inter",

                30,

                "bold"

            ),

            text_color=AXIOM_COLORS["text"]

        )


        self.title.pack()


        self.subtitle = ctk.CTkLabel(

            self.logo_frame,

            text="AI COMMAND CENTER",

            font=(

                "Inter",

                10,

                "bold"

            ),

            text_color=AXIOM_COLORS["muted"]

        )


        self.subtitle.pack(

            pady=(3, 0)

        )


        # ===============================
        # COLLAPSE BUTTON
        # ===============================


        self.toggle = ctk.CTkButton(

            self,

            text="☰",

            width=46,

            height=40,

            corner_radius=14,

            font=BUTTON_FONT,

            fg_color=AXIOM_COLORS["panel"],

            hover_color=AXIOM_COLORS["card_hover"],

            text_color=AXIOM_COLORS["text"],

            command=self.toggle_sidebar

        )


        self.toggle.pack(

            pady=10

        )


        # ===============================
        # NAVIGATION
        # ===============================


        self.nav = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )


        self.nav.pack(

            fill="both",

            expand=True,

            pady=20

        )


        pages = [

            ("⌂", "Home"),

            ("◉", "Chat"),

            ("◈", "Memory"),

            ("◷", "Tasks"),

            ("↻", "Updates"),

            ("⚙", "Debug"),

            ("⚙", "Settings"),

            ("✉", "Axiom Support")

        ]


        self.buttons = []


        for icon, name in pages:

            button = self.create_button(

                icon,

                name

            )

            self.buttons.append(button)


        # ===============================
        # STATUS
        # ===============================


        self.status = ctk.CTkFrame(

            self,

            fg_color=AXIOM_COLORS["panel"],

            corner_radius=18,

            border_width=1,

            border_color=AXIOM_COLORS["border"]

        )


        self.status.pack(

            fill="x",

            padx=15,

            pady=20

        )


        self.status_label = ctk.CTkLabel(

            self.status,

            text="● AI READY",

            font=(

                "Inter",

                12,

                "bold"

            ),

            text_color=AXIOM_COLORS["success"]

        )


        self.status_label.pack(

            pady=15

        )


    # ===============================
    # CREATE BUTTON
    # ===============================


    def create_button(

        self,

        icon,

        name

    ):


        button = ctk.CTkButton(

            self.nav,

            text=f"{icon}   {name}",

            height=SIDEBAR_BUTTON_HEIGHT,

            corner_radius=SIDEBAR_BUTTON_RADIUS,

            anchor="w",

            font=BUTTON_FONT,

            fg_color="transparent",

            hover_color=AXIOM_COLORS["card_hover"],

            text_color=AXIOM_COLORS["text"],

            command=lambda: self.select_page(

                button,

                name

            )

        )


        button.pack(

            fill="x",

            padx=15,

            pady=5

        )


        return button


    # ===============================
    # SELECT PAGE
    # ===============================


    def select_page(

        self,

        button,

        page

    ):


        if self.active_button:

            self.active_button.configure(

                fg_color="transparent",

                text_color=AXIOM_COLORS["text"]

            )


        button.configure(

            fg_color=AXIOM_COLORS["gold"],

            text_color=AXIOM_COLORS["black"]

        )


        self.active_button = button


        self.app.show_page(

            page

        )


    # ===============================
    # COLLAPSE
    # ===============================


    def toggle_sidebar(self):


        if self.expanded:

            self.configure(

                width=SIDEBAR_COLLAPSED

            )


            self.title.pack_forget()

            self.subtitle.pack_forget()


            self.status_label.configure(

                text="●"

            )


            for button in self.buttons:

                icon = button.cget(

                    "text"

                ).split()[0]

                button.configure(

                    text=icon,

                    anchor="center"

                )


            self.toggle.configure(

                text="→"

            )


            self.expanded = False


        else:

            self.configure(

                width=SIDEBAR_WIDTH

            )


            self.title.pack()

            self.subtitle.pack(

                pady=(3, 0)

            )


            self.status_label.configure(

                text="● AI READY"

            )


            pages = [

                ("⌂", "Home"),

                ("◉", "Chat"),

                ("◈", "Memory"),

                ("◷", "Tasks"),

                ("↻", "Updates"),

                ("⚙", "Debug"),

                ("⚙", "Settings"),

                ("✉", "Axiom Support")

            ]


            for button, data in zip(

                self.buttons,

                pages

            ):

                button.configure(

                    text=f"{data[0]}   {data[1]}",

                    anchor="w"

                )


            self.toggle.configure(

                text="☰"

            )


            self.expanded = True