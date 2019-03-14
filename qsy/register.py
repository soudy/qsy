class Register:
    def __init__(self, size):
        self.size = size
        self.state = []

    def __len__(self):
        return self.size

    def __repr__(self):
        return '{}<{}[{}]>'.format(self.__class__.__name__, self.name,
                                   self.size)
