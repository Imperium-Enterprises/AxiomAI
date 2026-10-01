import subprocess
import platform


class UpdateManager:


    def __init__(self):
        pass



    # =========================
    # CHECK WINDOWS UPDATE
    # =========================

    def check_updates(self):

        system = platform.system()


        if system != "Windows":

            return "Update checking is only supported on Windows."



        try:

            # Opens Windows update page
            subprocess.Popen(
                "start ms-settings:windowsupdate",
                shell=True
            )


            return (
                "I opened Windows Update. "
                "You can check for available updates there."
            )


        except Exception as e:


            return (
                f"I couldn't open Windows Update. Error: {e}"
            )



    # =========================
    # UPDATE COMPUTER
    # =========================

    def update_computer(self):


        return (
            "I can check updates, "
            "but automatic installation is not enabled yet."
        )