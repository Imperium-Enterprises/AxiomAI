import platform
import urllib.parse
import webbrowser

import customtkinter as ctk

from interface.theme import (
    AXIOM_COLORS,
    TITLE_FONT,
    HEADING_FONT,
    BODY_FONT,
    BUTTON_FONT,
    CARD_RADIUS
)

from core.axiom_support import AxiomSupport


class AxiomSupportPage(ctk.CTkFrame):

    def __init__(self, parent, brain):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.brain = brain

        self.support = AxiomSupport()

        self.build_page()

    # =====================================================
    # PAGE
    # =====================================================

    def build_page(self):

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

        # =================================================
        # HEADER
        # =================================================

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
            text="◆  AXIOM SUPPORT",
            font=TITLE_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            header,
            text="Get help, send feedback, or report an Axiom response.",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        self.status = ctk.CTkLabel(
            header,
            text="● SUPPORT CENTER READY",
            font=BODY_FONT,
            text_color=AXIOM_COLORS["success"]
        )

        self.status.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # =================================================
        # CONTACT SUPPORT
        # =================================================

        contact_card = self.create_card(
            "✉  CONTACT SUPPORT",
            "Need help with Axiom? Contact the Axiom support team directly."
        )

        contact_card.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkButton(
            contact_card,
            text="✉  CONTACT AXIOM SUPPORT",
            width=300,
            height=50,
            corner_radius=14,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            hover_color=AXIOM_COLORS["gold_hover"],
            text_color=AXIOM_COLORS["black"],
            command=self.contact_support
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 25)
        )

        # =================================================
        # FEEDBACK
        # =================================================

        feedback_card = self.create_card(
            "◆  SEND FEEDBACK",
            "Tell us what you like, what could be improved, or what you want added to Axiom."
        )

        feedback_card.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.feedback_box = ctk.CTkTextbox(
            feedback_card,
            height=150,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            border_width=1,
            border_color=AXIOM_COLORS["border"],
            corner_radius=14,
            text_color=AXIOM_COLORS["text"]
        )

        self.feedback_box.pack(
            fill="x",
            padx=25,
            pady=(15, 10)
        )

        ctk.CTkButton(
            feedback_card,
            text="SEND FEEDBACK",
            width=220,
            height=48,
            corner_radius=14,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            hover_color=AXIOM_COLORS["gold_hover"],
            text_color=AXIOM_COLORS["black"],
            command=self.send_feedback
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        # =================================================
        # REPORT RESPONSE
        # =================================================

        report_card = self.create_card(
            "⚠  REPORT AN AXIOM RESPONSE",
            "Report a response that was inappropriate, unsafe, offensive, harmful, or incorrect."
        )

        report_card.pack(
            fill="x",
            padx=40,
            pady=10
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        ctk.CTkLabel(
            report_card,
            text="What did Axiom say?",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 8)
        )

        self.response_box = ctk.CTkTextbox(
            report_card,
            height=140,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            border_width=1,
            border_color=AXIOM_COLORS["border"],
            corner_radius=14,
            text_color=AXIOM_COLORS["text"]
        )

        self.response_box.pack(
            fill="x",
            padx=25
        )

        # -------------------------------------------------
        # CONTEXT
        # -------------------------------------------------

        ctk.CTkLabel(
            report_card,
            text="What were you asking Axiom?",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        self.context_box = ctk.CTkTextbox(
            report_card,
            height=110,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            border_width=1,
            border_color=AXIOM_COLORS["border"],
            corner_radius=14,
            text_color=AXIOM_COLORS["text"]
        )

        self.context_box.pack(
            fill="x",
            padx=25
        )

        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

        ctk.CTkLabel(
            report_card,
            text="Additional details (optional)",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        self.details_box = ctk.CTkTextbox(
            report_card,
            height=110,
            font=BODY_FONT,
            fg_color=AXIOM_COLORS["panel"],
            border_width=1,
            border_color=AXIOM_COLORS["border"],
            corner_radius=14,
            text_color=AXIOM_COLORS["text"]
        )

        self.details_box.pack(
            fill="x",
            padx=25
        )

        # -------------------------------------------------
        # REPORT BUTTON
        # -------------------------------------------------

        ctk.CTkButton(
            report_card,
            text="⚠  SUBMIT REPORT",
            width=220,
            height=50,
            corner_radius=14,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["danger"],
            hover_color=AXIOM_COLORS["danger"],
            text_color=AXIOM_COLORS["text"],
            command=self.send_report
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 25)
        )

        # =================================================
        # SUPPORT & SAFETY INFORMATION
        # =================================================

        information_card = ctk.CTkFrame(
            self.content,
            fg_color=AXIOM_COLORS["panel"],
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )

        information_card.pack(
            fill="x",
            padx=40,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            information_card,
            text="◆  WHAT YOU CAN DO HERE",
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 8)
        )

        ctk.CTkLabel(
            information_card,
            text=(
                "The Axiom Support Center provides a dedicated place "
                "for users to get assistance, provide feedback, and "
                "report problematic AI behavior."
            ),
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text"],
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # SUPPORT ITEM
        # -------------------------------------------------

        self.create_info_row(
            information_card,
            "✉",
            "Get Support",
            "Contact Axiom Support when you need assistance with the application."
        )

        # -------------------------------------------------
        # FEEDBACK ITEM
        # -------------------------------------------------

        self.create_info_row(
            information_card,
            "◆",
            "Send Feedback",
            "Share suggestions, improvements, feature requests, or general feedback."
        )

        # -------------------------------------------------
        # SAFETY REPORT ITEM
        # -------------------------------------------------

        self.create_info_row(
            information_card,
            "⚠",
            "Report Inappropriate Responses",
            (
                "If Axiom produces an inappropriate, unsafe, offensive, "
                "harmful, or otherwise problematic response, use the "
                "Report an Axiom Response section above to submit it "
                "for review."
            )
        )

        # -------------------------------------------------
        # SAFETY NOTE
        # -------------------------------------------------

        safety_note = ctk.CTkFrame(
            information_card,
            fg_color=AXIOM_COLORS["card"],
            corner_radius=14,
            border_width=1,
            border_color=AXIOM_COLORS["border"]
        )

        safety_note.pack(
            fill="x",
            padx=25,
            pady=(10, 25)
        )

        ctk.CTkLabel(
            safety_note,
            text="⚠  SAFETY REPORTING",
            font=BUTTON_FONT,
            text_color=AXIOM_COLORS["danger"]
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            safety_note,
            text=(
                "Users are encouraged to report concerning AI behavior "
                "through this support center. Reports can include the "
                "Axiom response, the user's original question, and "
                "additional details to help with investigation."
            ),
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"],
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        # =================================================
        # BOTTOM SPACE
        # =================================================

        ctk.CTkFrame(
            self.content,
            height=30,
            fg_color="transparent"
        ).pack()

    # =====================================================
    # CARD CREATOR
    # =====================================================

    def create_card(
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
            text_color=AXIOM_COLORS["text_secondary"],
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=25
        )

        return card

    # =====================================================
    # INFORMATION ROW
    # =====================================================

    def create_info_row(
        self,
        parent,
        icon,
        title,
        description
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=7
        )

        icon_label = ctk.CTkLabel(
            row,
            text=icon,
            width=35,
            font=(
                "Inter",
                20,
                "bold"
            ),
            text_color=AXIOM_COLORS["gold"]
        )

        icon_label.pack(
            side="left",
            anchor="n",
            padx=(0, 10)
        )

        text_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=BUTTON_FONT,
            text_color=AXIOM_COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            text_frame,
            text=description,
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text_secondary"],
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            pady=(2, 5)
        )

    # =====================================================
    # CONTACT SUPPORT
    # =====================================================

    def contact_support(self):

        support_email = self.support.get_support_email()

        subject = urllib.parse.quote(
            "Axiom Support Request"
        )

        body = urllib.parse.quote(
            "Hello Axiom Support,\n\n"
            "I need assistance with Axiom.\n\n"
            "Issue:\n\n"
            "Additional information:\n\n"
        )

        mailto = (
            f"mailto:{support_email}"
            f"?subject={subject}"
            f"&body={body}"
        )

        try:

            opened = webbrowser.open(
                mailto
            )

            if opened:

                self.set_status(
                    "● SUPPORT EMAIL READY",
                    AXIOM_COLORS["success"]
                )

            else:

                self.show_message(
                    "Unable to Open Email",
                    "Could not open your default email application."
                )

        except Exception as e:

            self.show_message(
                "Unable to Open Email",
                f"Could not open your email application.\n\n{e}"
            )

    # =====================================================
    # FEEDBACK
    # =====================================================

    def send_feedback(self):

        message = self.feedback_box.get(
            "1.0",
            "end"
        ).strip()

        if not message:

            self.show_message(
                "Feedback Required",
                "Please enter some feedback before submitting."
            )

            return

        try:

            success = self.support.send_feedback(
                message
            )

            if success:

                self.feedback_box.delete(
                    "1.0",
                    "end"
                )

                self.set_status(
                    "● FEEDBACK SENT",
                    AXIOM_COLORS["success"]
                )

                self.show_message(
                    "Feedback Sent",
                    "Thank you. Your feedback has been sent to Axiom Support."
                )

            else:

                self.show_message(
                    "Feedback Failed",
                    "Axiom could not send your feedback. Please try again."
                )

        except Exception as e:

            print(
                "Feedback UI error:",
                e
            )

            self.show_message(
                "Feedback Failed",
                "Axiom could not send your feedback."
            )

    # =====================================================
    # REPORT
    # =====================================================

    def send_report(self):

        response = self.response_box.get(
            "1.0",
            "end"
        ).strip()

        context = self.context_box.get(
            "1.0",
            "end"
        ).strip()

        details = self.details_box.get(
            "1.0",
            "end"
        ).strip()

        if not response:

            self.show_message(
                "Report Required",
                "Please enter what Axiom said."
            )

            return

        try:

            success = self.support.send_report(
                response=response,
                context=context,
                details=details,
                version="1.0",
                os_name=platform.system(),
                os_version=platform.release(),
                python_version=platform.python_version()
            )

            if success:

                self.response_box.delete(
                    "1.0",
                    "end"
                )

                self.context_box.delete(
                    "1.0",
                    "end"
                )

                self.details_box.delete(
                    "1.0",
                    "end"
                )

                self.set_status(
                    "● REPORT SENT",
                    AXIOM_COLORS["success"]
                )

                self.show_message(
                    "Report Sent",
                    "Thank you. Your report has been submitted to Axiom Support."
                )

            else:

                self.show_message(
                    "Report Failed",
                    "Axiom could not send your report. Please try again."
                )

        except Exception as e:

            print(
                "Report UI error:",
                e
            )

            self.show_message(
                "Report Failed",
                "Axiom could not send your report."
            )

    # =====================================================
    # STATUS
    # =====================================================

    def set_status(
        self,
        text,
        color
    ):

        self.status.configure(
            text=text,
            text_color=color
        )

        self.after(
            3000,
            self.reset_status
        )

    def reset_status(self):

        self.status.configure(
            text="● SUPPORT CENTER READY",
            text_color=AXIOM_COLORS["success"]
        )

    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(
        self,
        title,
        message
    ):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            title
        )

        dialog.geometry(
            "500x250"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=AXIOM_COLORS["background"]
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=title,
            font=HEADING_FONT,
            text_color=AXIOM_COLORS["gold"]
        ).pack(
            pady=(35, 15)
        )

        ctk.CTkLabel(
            dialog,
            text=message,
            font=BODY_FONT,
            text_color=AXIOM_COLORS["text"],
            wraplength=420,
            justify="center"
        ).pack(
            padx=30
        )

        ctk.CTkButton(
            dialog,
            text="OK",
            width=140,
            height=45,
            corner_radius=14,
            font=BUTTON_FONT,
            fg_color=AXIOM_COLORS["gold"],
            hover_color=AXIOM_COLORS["gold_hover"],
            text_color=AXIOM_COLORS["black"],
            command=dialog.destroy
        ).pack(
            pady=25
        )