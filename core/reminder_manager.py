import json
import os
import threading
from datetime import datetime

from core.paths import REMINDERS_FILE


class ReminderManager:


    def __init__(self, speak_callback):

        self.speak = speak_callback

        self.lock = threading.Lock()

        self.file = REMINDERS_FILE


        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )


        if not os.path.exists(self.file):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )



    def load_reminders(self):

        try:

            with open(
                self.file,
                "r"
            ) as f:

                return json.load(f)


        except Exception:

            return []




    def save_reminders(self, reminders):

        with open(
            self.file,
            "w"
        ) as f:


            json.dump(
                reminders,
                f,
                indent=4
            )




    def add_reminder(
        self,
        date_string,
        reminder_text
    ):


        with self.lock:


            reminders = self.load_reminders()


            reminders.append(

                {

                    "datetime": date_string,

                    "text": reminder_text,

                    "completed": False

                }

            )


            self.save_reminders(
                reminders
            )




    def check_reminders(self):


        with self.lock:


            reminders = self.load_reminders()

            now = datetime.now()

            changed = False



            for reminder in reminders:


                if reminder.get(
                    "completed",
                    False
                ):

                    continue



                try:

                    reminder_time = datetime.strptime(

                        reminder["datetime"],

                        "%Y-%m-%d %H:%M"

                    )


                except Exception:

                    reminder["completed"] = True

                    changed = True

                    continue




                if reminder_time <= now:


                    if reminder_time.date() == now.date():


                        message = (

                            "Boss, here's your reminder. "

                            +

                            reminder["text"]

                        )


                    else:


                        message = (

                            "Boss, you missed a reminder from "

                            +

                            reminder_time.strftime(

                                "%B %d %Y"

                            )

                            +

                            ". "

                            +

                            reminder["text"]

                        )



                    reminder["completed"] = True

                    changed = True



                    self.save_reminders(
                        reminders
                    )


                    self.speak(
                        message
                    )





            if changed:


                reminders = [

                    r for r in reminders

                    if not (

                        r.get(
                            "completed"
                        )

                        and

                        (

                            now -

                            datetime.strptime(

                                r["datetime"],

                                "%Y-%m-%d %H:%M"

                            )

                        ).days > 30

                    )

                ]



                self.save_reminders(
                    reminders
                )