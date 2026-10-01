import json
import os

from core.paths import SETTINGS_FILE


class SettingsManager:


    def __init__(self):

        os.makedirs(
            os.path.dirname(SETTINGS_FILE),
            exist_ok=True
        )


        self.file = SETTINGS_FILE



        if not os.path.exists(self.file):

            self.save({

                "voice_enabled": True,
                "personality": "Sarcastic",
                "response_style": "Balanced"

            })




    def load(self):

        try:

            with open(
                self.file,
                "r"
            ) as f:

                return json.load(f)



        except:


            default = {

                "voice_enabled": True,
                "personality": "Sarcastic",
                "response_style": "Balanced"

            }


            self.save(
                default
            )


            return default





    def save(self, data):


        with open(
            self.file,
            "w"
        ) as f:


            json.dump(

                data,

                f,

                indent=4

            )