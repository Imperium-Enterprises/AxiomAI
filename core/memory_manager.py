import json
import os

from core.paths import MEMORY_FILE


class MemoryManager:


    def __init__(self):

        self.memory_file = MEMORY_FILE


        os.makedirs(
            os.path.dirname(self.memory_file),
            exist_ok=True
        )


        # Create file if missing
        if not os.path.exists(self.memory_file):

            with open(
                self.memory_file,
                "w"
            ) as f:

                json.dump(
                    {},
                    f
                )



    def load_memory(self):

        try:

            with open(
                self.memory_file,
                "r"
            ) as f:

                return json.load(f)


        except Exception:

            return {}




    def save_memory(self, data):

        try:

            with open(
                self.memory_file,
                "w"
            ) as f:


                json.dump(
                    data,
                    f,
                    indent=4
                )


        except Exception as e:

            print(
                "Memory save error:",
                e
            )




    def remember(self, key, value):

        memory = self.load_memory()

        memory[key] = value

        self.save_memory(
            memory
        )




    def recall(self, key):

        memory = self.load_memory()

        return memory.get(key)