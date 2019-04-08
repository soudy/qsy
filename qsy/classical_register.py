import itertools
from .register import Register


class ClassicalRegister(Register):
    instance_counter = itertools.count()
    prefix = 'c'

    def __init__(self, size, name=None):
        super().__init__(size, name)
        self.state = [0] * size

    def set_state(self, state):
        self.state = state

    def __getitem__(self, index):
        return self.state[index]

    def __setitem__(self, index, value):
        self.state[index] = value
