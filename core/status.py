import os
import json


class AxiomStatus:


    def get_status(self):

        return {

            "brain": "ONLINE",

            "ollama": self.check_ollama(),

            "memory": self.get_memory(),

            "apps": self.get_apps(),

            "reminders": self.get_reminders()

        }



    def check_ollama(self):

        try:

            import ollama

            ollama.list()

            return "ONLINE"


        except:

            return "OFFLINE"



    def get_memory(self):

        try:

            with open(
                "memory/memory.json",
                "r"
            ) as f:

                data = json.load(f)

                return f"{len(data)} items"


        except:

            return "0 items"



    def get_apps(self):

        try:

            with open(
                "apps.json",
                "r"
            ) as f:

                data = json.load(f)

                return f"{len(data)} apps"


        except:

            return "0 apps"



    def get_reminders(self):

        try:

            with open(
                "memory/reminders.json",
                "r"
            ) as f:

                data = json.load(f)

                return f"{len(data)} reminders"


        except:

            return "0 reminders"