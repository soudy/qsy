import itertools


class Register:
    instance_counter = itertools.count()
    prefix = 'r'

    def __init__(self, size, name=None):
        if size <= 0 or not isinstance(size, int):
            raise Exception('Invalid register size "{}"'.format(size))

        self.size = size

        if name is None:
            name = '{}{}'.format(self.prefix, next(self.instance_counter))

        self.name = name

    def __len__(self):
        return self.size

    def __repr__(self):
        return '{}[{}]'.format(self.name, self.size)
