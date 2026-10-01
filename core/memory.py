import os
import json


class Memory:

    def __init__(self):

        self.memory_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "memory",
            "session_memory.json"
        )

        # Make sure memory folder exists
        os.makedirs(
            os.path.dirname(self.memory_file),
            exist_ok=True
        )

        self.data = {}

        self.load()


    # =========================
    # LOAD MEMORY
    # =========================

    def load(self):

        try:

            if os.path.exists(self.memory_file):

                with open(
                    self.memory_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.data = json.load(file)

            else:

                self.data = {}

                self.save()


        except Exception as e:

            print(
                "Memory load error:",
                e
            )

            self.data = {}



    # =========================
    # SAVE MEMORY
    # =========================

    def save(self):

        try:

            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


        except Exception as e:

            print(
                "Memory save error:",
                e
            )



    # =========================
    # REMEMBER
    # =========================

    def remember(
        self,
        key,
        value
    ):

        if not key:

            return False


        self.data[key] = value

        self.save()

        return True



    # =========================
    # RECALL
    # =========================

    def recall(
        self,
        key
    ):

        return self.data.get(
            key,
            None
        )



    # =========================
    # FORGET ONE MEMORY
    # =========================

    def forget(
        self,
        key
    ):

        if key in self.data:

            del self.data[key]

            self.save()

            return True


        return False



    # =========================
    # CLEAR ALL MEMORY
    # =========================

    def clear(self):

        self.data = {}

        self.save()

        return True