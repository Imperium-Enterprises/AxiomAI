import json
import os
import sys
import time

from vosk import Model, KaldiRecognizer



class WakeWordListener:


    def __init__(self):


        self.wake_words = [

            [
                "terminal",
                "start"
            ],

            [
                "axiom",
                "start"
            ],

            [
                "axiom"
            ]

        ]



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

                "Wake word model folder is missing."

            )



        print(

            "Loading wake word model..."

        )



        self.model = Model(

            model_path

        )



        self.recognizer = KaldiRecognizer(

            self.model,

            16000

        )


        self.recognizer.SetWords(True)



        print(

            "Wake word model loaded."

        )







    # =========================
    # LISTEN FOR WAKE WORD
    # =========================


    def listen_for_wake_word(self, microphone):


        print(

            "👂 Listening for wake word..."

        )



        microphone.clear_queue()



        self.recognizer.Reset()



        start_time = time.time()



        while True:



            # prevent infinite lock

            if time.time() - start_time > 60:


                return False





            try:


                data = microphone.get_audio_chunk()



                if data is None:

                    continue



            except Exception as e:


                print(

                    "Wake word audio error:",

                    e

                )


                continue





            if self.recognizer.AcceptWaveform(data):



                result = json.loads(

                    self.recognizer.Result()

                )



                text = result.get(

                    "text",

                    ""

                ).lower().strip()





                if text:


                    print(

                        "RAW HEARD:",

                        text

                    )





                    for words in self.wake_words:



                        if all(

                            word in text

                            for word in words

                        ):



                            print(

                                "🔥 WAKE WORD DETECTED"

                            )



                            self.recognizer.Reset()



                            microphone.clear_queue()



                            return True