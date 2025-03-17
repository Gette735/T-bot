class StateMachine(object):
    def __init__(self, name):
        self.name = name
        self.current_state = ""
        self.prev_state = ""
        self.new_state = "init"
        self._process()

    def _process(self):
        self.update_state()
        self.process_state()

    def update_state(self):
        if self.new_state != "":
            if self.new_state != self.current_state:
                init_method = "__init__" + self.new_state
                end_method = "__end__" + self.current_state

                if hasattr(self, end_method):
                    getattr(self, end_method)()

                if hasattr(self, init_method):
                    getattr(self, init_method)()

                self.prev_state = self.current_state
                self.current_state = self.new_state

    def return_state(self):
        if self.prev_state is not None:
            self.current_state = self.prev_state

    def process_state(self):
        state_method = "_" + self.current_state
        if hasattr(self, state_method):
            getattr(self, state_method)()