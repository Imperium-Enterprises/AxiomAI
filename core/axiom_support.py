import os
import platform
import urllib.parse
import webbrowser

import requests


class AxiomSupport:
    """
    Handles all Axiom support communication.

    Includes:
    - Contact Support
    - User Feedback
    - Safety / Response Reports
    """

    SUPPORT_EMAIL = "IE.ImperiumEnterprises@gmail.com"

    def __init__(self):
        self.backend_url = os.environ.get(
            "AXIOM_BACKEND_URL",
            ""
        ).strip().rstrip("/")

        self.api_key = os.environ.get(
            "AXIOM_API_KEY",
            ""
        ).strip()

    # =====================================================
    # CONTACT SUPPORT
    # =====================================================

    def contact_support(self):
        subject = urllib.parse.quote(
            "Axiom Support Request"
        )

        body = urllib.parse.quote(
            "Hello Axiom Support,\n\n"
            "I need assistance with Axiom.\n\n"
            "Issue:\n\n\n"
            "Additional information:\n\n\n"
        )

        mailto = (
            f"mailto:{self.SUPPORT_EMAIL}"
            f"?subject={subject}"
            f"&body={body}"
        )

        return webbrowser.open(mailto)

    # =====================================================
    # SEND FEEDBACK
    # =====================================================

    def send_feedback(self, message):
        if not message or not message.strip():
            return False

        payload = {
            "message": message.strip(),
            "version": "1.0",
            "os_name": platform.system(),
            "os_version": platform.release(),
            "python_version": platform.python_version()
        }

        return self._send_request(
            "/feedback",
            payload
        )

    # =====================================================
    # REPORT RESPONSE
    # =====================================================

    def send_report(
        self,
        response,
        context="",
        details=""
    ):
        if not response or not response.strip():
            return False

        payload = {
            "response": response.strip(),
            "context": (
                context.strip()
                if context
                else ""
            ),
            "details": (
                details.strip()
                if details
                else ""
            ),
            "version": "1.0",
            "os_name": platform.system(),
            "os_version": platform.release(),
            "python_version": platform.python_version()
        }

        return self._send_request(
            "/report",
            payload
        )

    # =====================================================
    # BACKEND REQUEST
    # =====================================================

    def _send_request(
        self,
        endpoint,
        payload
    ):
        if not self.backend_url:
            print(
                "Axiom Support: "
                "AXIOM_BACKEND_URL is not configured."
            )

            return False

        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["X-Axiom-Api-Key"] = self.api_key

        try:
            response = requests.post(
                f"{self.backend_url}{endpoint}",
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    return False

                return data.get(
                    "success",
                    False
                )

            print(
                "Axiom Support server error:",
                response.status_code,
                response.text
            )

            return False

        except requests.exceptions.Timeout:
            print(
                "Axiom Support connection timed out."
            )

            return False

        except requests.exceptions.ConnectionError:
            print(
                "Axiom Support connection failed."
            )

            return False

        except requests.RequestException as e:
            print(
                "Axiom Support request error:",
                e
            )

            return False

        except Exception as e:
            print(
                "Axiom Support error:",
                e
            )

            return False