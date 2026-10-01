import customtkinter as ctk

from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BODY_FONT,
    BUTTON_FONT,
    CARD_RADIUS
)


class SettingsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        brain
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.brain = brain

        self.manager = brain.settings

        self.settings = self.manager.load()

        # =========================================================
        # MAIN SCROLL AREA
        # =========================================================

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=AXIOM_COLORS["border"],
            scrollbar_button_hover_color=AXIOM_COLORS["gold"]
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True
        )

        self.content = self.scroll_frame

        # =========================================================
        # HEADER
        # =========================================================

        header = ctk.CTkFrame(
            self.content,
            fg_color=AXIOM_COLORS["panel"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(35, 20)
        )

        ctk.CTkLabel(
            header,
            text="⚙  AXIOM CONTROL CENTER",
            font=TITLE_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            header,
            text="Configure your personal AI assistant",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        self.status = ctk.CTkLabel(
            header,
            text="● CONFIGURATION READY",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["success"]
        )

        self.status.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # =========================================================
        # VOICE SETTINGS
        # =========================================================

        voice_card = self.create_setting_card(
            "◉  VOICE SYSTEM",
            "Control Axiom speech responses"
        )

        voice_card.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.voice = ctk.CTkSwitch(
            voice_card,
            text="Voice Enabled",
            font=BODY_FONT,
            progress_color=AXIOM_COLORS["gold"],
            button_color=AXIOM_COLORS["gold"],
            button_hover_color=AXIOM_COLORS["gold_hover"]
        )

        self.voice.pack(
            anchor="w",
            padx=25,
            pady=20
        )

        if self.settings.get(
            "voice_enabled",
            True
        ):
            self.voice.select()

        # =========================================================
        # PERSONALITY
        # =========================================================

        personality_card = self.create_setting_card(
            "◆  PERSONALITY PROFILE",
            "Choose how Axiom communicates"
        )

        personality_card.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.personality = ctk.CTkOptionMenu(
            personality_card,
            values=[
                "Sarcastic",
                "Professional",
                "Friendly"
            ],
            width=280,
            height=45,
            corner_radius=14,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            button_color=AXIOM_COLORS["gold"],
            button_hover_color=AXIOM_COLORS["gold_hover"],
            text_color=AXIOM_COLORS["text"]
        )

        self.personality.pack(
            anchor="w",
            padx=25,
            pady=20
        )

        self.personality.set(
            self.settings.get(
                "personality",
                "Sarcastic"
            )
        )

        # =========================================================
        # SAVE BUTTON
        # =========================================================

        self.save_button = ctk.CTkButton(
            self.content,
            text="SAVE CONFIGURATION",
            width=320,
            height=60,
            corner_radius=16,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            hover_color=AXIOM_COLORS["gold_hover"],
            text_color=AXIOM_COLORS["black"],
            command=self.save_settings
        )

        self.save_button.pack(
            pady=35
        )

    # =========================================================
    # SETTING CARD
    # =========================================================

    def create_setting_card(
        self,
        title,
        description
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=description,
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        return card

    # =========================================================
    # SAVE SETTINGS
    # =========================================================

    def save_settings(self):

        self.settings["voice_enabled"] = bool(
            self.voice.get()
        )

        self.settings["personality"] = (
            self.personality.get()
        )

        self.manager.save(
            self.settings
        )

        self.brain.config = self.settings

        self.brain.system = {
            "role": "system",
            "content": (
                self.brain.build_personality_prompt()
            )
        }

        self.status.configure(
            text="● SETTINGS UPDATED",
            text_color=AXIOM_COLORS["success"]
        )

        self.save_button.configure(
            text="✓ SAVED"
        )

        self.after(
            2500,
            self.reset_status
        )

    # =========================================================
    # RESET STATUS
    # =========================================================

    def reset_status(self):

        self.status.configure(
            text="● CONFIGURATION READY",
            text_color=AXIOM_COLORS["success"]
        )

        self.save_button.configure(
            text="SAVE CONFIGURATION"
        )