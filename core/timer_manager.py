import threading
import time


class TimerManager:

    def __init__(self, speak_callback):

        self.speak = speak_callback
        self.timers = []


    def set_timer(self, seconds):

        if seconds <= 0:

            return False


        timer = threading.Timer(
            seconds,
            self.timer_finished
        )


        timer.start()


        self.timers.append(
            timer
        )


        return True



    def timer_finished(self):

        self.speak(
            "Boss, your timer is up."
        )


        self.cleanup()



    def cleanup(self):

        self.timers = [
            timer
            for timer in self.timers
            if timer.is_alive()
        ]



    def cancel_all(self):

        for timer in self.timers:

            timer.cancel()


        self.timers.clear()