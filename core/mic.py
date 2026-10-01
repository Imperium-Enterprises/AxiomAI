import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import time
import os
import sys


class Microphone:


    def __init__(self, brain):


        if getattr(sys, "frozen", False):

            base_path = sys._MEIPASS

        else:

            base_path = os.path.dirname(
                os.path.dirname(__file__)
            )


        model_path = os.path.join(
            base_path,
            "model"
        )


        if not os.path.exists(model_path):

            raise FileNotFoundError(
                "Vosk model folder was not found."
            )


        print(
            "Loading voice model..."
        )


        self.model = Model(
            model_path
        )


        self.brain = brain


        self.rec = KaldiRecognizer(
            self.model,
            16000
        )


        self.rec.SetWords(True)



        # NORMAL AUDIO PIPE

        self.audio_queue = queue.Queue(
            maxsize=200
        )


        # INTERRUPT AUDIO PIPE

        self.interrupt_q = queue.Queue(
            maxsize=200
        )



        self.stream = None


        self.running = False



        print(
            "Voice model loaded."
        )





    # =========================
    # AUDIO CALLBACK
    # =========================


    def callback(
        self,
        indata,
        frames,
        time_info,
        status
    ):


        if status:

            print(
                "Mic status:",
                status
            )


        audio = bytes(indata)



        try:

            self.audio_queue.put_nowait(
                audio
            )


        except queue.Full:

            pass



        try:

            self.interrupt_q.put_nowait(
                audio
            )


        except queue.Full:

            pass







    # =========================
    # START
    # =========================


    def start(self):


        if self.running:

            return



        self.running = True



        self.stream = sd.RawInputStream(

            samplerate=16000,

            blocksize=1024,

            dtype="int16",

            channels=1,

            callback=self.callback

        )


        self.stream.start()



        print(
            "🎤 Microphone started"
        )







    # =========================
    # CLEAR AUDIO
    # =========================


    def clear_queue(self):


        removed = 0


        while not self.audio_queue.empty():

            try:

                self.audio_queue.get_nowait()

                removed += 1


            except queue.Empty:

                break



        while not self.interrupt_q.empty():

            try:

                self.interrupt_q.get_nowait()


            except queue.Empty:

                break



        if removed:

            print(
                f"🎤 Cleared {removed} audio chunks"
            )







    # =========================
    # NORMAL LISTEN
    # =========================


    def listen(self):


        print(
            "🎤 Listening..."
        )


        self.rec.Reset()



        start = time.time()


        heard = False


        last_voice = time.time()



        while True:



            if time.time() - start > 10:

                return ""



            try:


                data = self.audio_queue.get(

                    timeout=0.05

                )


            except queue.Empty:

                continue






            if self.rec.AcceptWaveform(data):


                result = json.loads(

                    self.rec.Result()

                )


                text = result.get(

                    "text",

                    ""

                ).strip()



                if text:


                    print(

                        "HEARD:",

                        text

                    )



                    if self.brain.last_spoken:


                        spoken = self.brain.last_spoken.lower()

                        heard_text = text.lower()



                        if (

                            heard_text in spoken

                            or

                            spoken in heard_text

                        ):


                            print(

                                "IGNORED ECHO:",

                                text

                            )


                            self.rec.Reset()

                            continue





                    if len(text) >= 2:

                        return text


            else:


                partial = json.loads(

                    self.rec.PartialResult()

                ).get(

                    "partial",

                    ""

                )


                if partial:


                    heard = True

                    last_voice = time.time()





            if heard and time.time() - last_voice > 0.4:


                result = json.loads(

                    self.rec.FinalResult()

                )


                text = result.get(

                    "text",

                    ""

                ).strip()



                if text:


                    print(

                        "HEARD:",

                        text

                    )


                    return text







    # =========================
    # INTERRUPT LISTENER
    # =========================


    def listen_for_interrupt(self, interrupt_words):


        print(
            "🎧 Interrupt listener active"
        )


        interrupt_rec = KaldiRecognizer(

            self.model,

            16000

        )


        interrupt_rec.SetWords(True)


        interrupt_rec.Reset()



        while self.brain.speaking_event.is_set():



            try:


                data = self.interrupt_q.get(

                    timeout=0.05

                )


            except queue.Empty:


                continue





            if interrupt_rec.AcceptWaveform(data):


                result = json.loads(

                    interrupt_rec.Result()

                )


                text = result.get(

                    "text",

                    ""

                ).lower().strip()





                if text:


                    print(

                        "INTERRUPT CHECK:",

                        text

                    )


                    for word in interrupt_words:


                        if word in text:


                            print(

                                "🛑 INTERRUPT DETECTED:",

                                word

                            )


                            return True





            else:


                partial = json.loads(

                    interrupt_rec.PartialResult()

                ).get(

                    "partial",

                    ""

                ).lower()





                if partial:


                    for word in interrupt_words:


                        if word in partial:


                            print(

                                "🛑 INTERRUPT DETECTED:",

                                word

                            )


                            return True





        return False







    # =========================
    # WAKE WORD SUPPORT
    # =========================


    def get_audio_chunk(self):


        try:

            return self.audio_queue.get(

                timeout=0.1

            )


        except queue.Empty:

            return None







    # =========================
    # STOP
    # =========================


    def stop(self):


        self.running = False



        if self.stream:


            self.stream.stop()


            self.stream.close()


            self.stream = None



        print(

            "🎤 Microphone stopped"

        )