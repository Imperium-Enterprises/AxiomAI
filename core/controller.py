import threading
import time

from core.wake_word import WakeWordListener
from core.mic import Microphone
from core.state import state
from core.logger import logger


class AxiomController:


    def __init__(self, brain):


        logger.log(
            "Starting Axiom controller..."
        )


        self.brain = brain


        # Wake word

        self.wake = WakeWordListener()


        # Microphone

        self.microphone = Microphone(
            self.brain
        )


        self.running = True

        self.microphone.start()

        threading.Thread(
            target=self.interrupt_loop,
            daemon=True
        ).start()


        self.thread = None


        self.thinking = False


        self.conversation_mode = False


        self.last_command_time = 0


        self.speech_finished_time = 0



        self.interrupt_words = [

            "stop",
            "cancel",
            "quiet",
            "be quiet",
            "shut up",
            "stop talking"

        ]





    # =========================
    # START
    # =========================


    def start(self):


        if self.thread:

            return



        self.thread = threading.Thread(

            target=self.voice_loop,

            daemon=True

        )


        self.thread.start()



        logger.log(

            "Voice system started"

        )





    def interrupt_loop(self):

        while self.running:

            self.brain.speaking_event.wait()

            if not self.running:
                break
    
            interrupted = self.microphone.listen_for_interrupt(
                self.interrupt_words
            )

            if interrupted:

                logger.log("Voice interrupt detected")

                self.brain.stop_speaking()

                self.microphone.clear_queue()

                self.speech_finished_time = time.time()







    # =========================
    # VOICE LOOP
    # =========================


    def voice_loop(self):


        while self.running:



            if state.is_suspended():


                self.microphone.clear_queue()

                time.sleep(0.2)

                continue





            # =========================
            # WAKE WORD
            # =========================


            if not state.is_awake():


                try:


                    detected = self.wake.listen_for_wake_word(

                        self.microphone

                    )


                    if not detected:

                        continue



                except Exception as e:


                    logger.log(

                        f"Wake error: {e}"

                    )

                    time.sleep(1)

                    continue





                self.conversation_mode = True


                state.wake()


                self.brain.resume()



                self.microphone.clear_queue()



                self.brain.speak(

                    "Yeah?"

                )



                while self.brain.speaking_event.is_set():

                    time.sleep(0.01)



                self.microphone.clear_queue()



                self.speech_finished_time = time.time()


                # Don't listen for commands while speaking.
                # interrupt_loop handles speech interruption.
                if self.brain.speaking_event.is_set():
                    time.sleep(0.01)
                    continue











            # =========================
            # ECHO COOLDOWN
            # =========================


            if self.speech_finished_time:


                if time.time() - self.speech_finished_time < 0.4:


                    self.microphone.clear_queue()

                    time.sleep(0.05)

                    continue



                self.speech_finished_time = 0



            # =========================
            # NORMAL LISTEN
            # =========================


            try:


                command = self.microphone.listen()



            except Exception as e:


                logger.log(

                    f"Microphone error: {e}"

                )


                time.sleep(0.5)

                continue





            if not command:

                continue





            command_lower = command.lower().strip()



            print(

                "VOICE COMMAND:",

                command_lower

            )



            self.last_command_time = time.time()





            # =========================
            # INTERRUPT FALLBACK
            # =========================


            if any(

                word in command_lower

                for word in self.interrupt_words

            ):


                self.brain.stop_speaking()


                self.microphone.clear_queue()


                continue






            # =========================
            # SLEEP
            # =========================


            if command_lower == "sleep":


                self.brain.speak(

                    "Going to sleep."

                )



                while self.brain.speaking_event.is_set():

                    time.sleep(0.01)




                self.conversation_mode = False


                state.sleep()



                self.microphone.clear_queue()



                continue







            # =========================
            # PROCESS COMMAND
            # =========================


            if not self.thinking:


                self.thinking = True



                threading.Thread(

                    target=self.process_command,

                    args=(command,),

                    daemon=True

                ).start()








            # =========================
            # AUTO SLEEP
            # =========================


            if (

                self.conversation_mode

                and

                time.time() - self.last_command_time > 15

            ):


                self.conversation_mode = False


                state.sleep()







    # =========================
    # PROCESS COMMAND
    # =========================


    def process_command(self, command):


        try:


            self.brain.think(

                command

            )



        except Exception as e:


            logger.log(

                f"Brain error: {e}"

            )



        finally:



            while self.brain.speaking_event.is_set():

                time.sleep(0.05)




            time.sleep(0.5)



            self.microphone.clear_queue()



            self.speech_finished_time = time.time()



            self.thinking = False







    # =========================
    # SHUTDOWN
    # =========================


    def shutdown(self):


        logger.log(

            "Shutting down Axiom..."

        )



        self.running = False



        self.conversation_mode = False





        try:


            self.brain.stop_speaking()



        except:


            pass





        try:


            self.microphone.stop()



        except:


            pass