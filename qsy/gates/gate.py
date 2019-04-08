import collections

Gate = collections.namedtuple('Gate', ['name', 'matrix', 'arity'])


def C(gate):
    """Create a controlled-U gate."""
    return Gate('C{}'.format(gate.name), gate.matrix, 2)


def CC(gate):
    """Create a controlled-controlled-U gate."""
    return Gate('CC{}'.format(gate.name), gate.matrix, 3)
