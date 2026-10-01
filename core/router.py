class AxiomRouter:

    def __init__(self):
        self.commands = {
            "open ": "open_app",
            "close ": "close_app",
            "open folder ": "open_folder",
            "remind me": "reminder",
            "set a timer": "timer",
            "run system check": "system_check",
            "locate the website": "website"
        }


    def route(self, text):

        if not text:
            return None


        lower = text.lower().strip()


        for trigger, command in self.commands.items():

            if lower.startswith(trigger):

                return {
                    "type": command,
                    "text": text
                }


        return {
            "type": "chat",
            "text": text
        }