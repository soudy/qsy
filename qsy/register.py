import itertools


class Register:
    instance_counter = itertools.count()
    prefix = 'r'

    def __init__(self, size, name=None):
        self.size = size
        self.state = []

        if name is None:
            name = '{}{}'.format(self.prefix, next(self.instance_counter))

        self.name = name

    def __len__(self):
        return self.size

    def __repr__(self):
        return '{}<{}>'.format(self.__class__.__name__, self.size)
