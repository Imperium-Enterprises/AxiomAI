class AxiomState:


    def __init__(self):

        self.awake = False
        self.running = True
        self.suspended = False



    def sleep(self):

        self.awake = False



    def wake(self):

        if not self.suspended:
            self.awake = True



    def toggle(self):

        self.awake = not self.awake



    def is_awake(self):

        return self.awake



    def suspend(self):

        self.suspended = True
        self.awake = False



    def resume(self):

        self.suspended = False



    def is_suspended(self):

        return self.suspended



state = AxiomState()