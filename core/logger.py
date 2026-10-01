import time


class AxiomLogger:

    def __init__(self):

        self.logs = []



    def log(self, message):

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        entry = (
            f"[{timestamp}] {message}"
        )

        print(entry)

        self.logs.append(
            entry
        )


    def get_logs(self):

        return self.logs[-100:]



# Global logger
logger = AxiomLogger()