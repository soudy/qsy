import collections

Gate = collections.namedtuple(
    'Gate', ['name', 'matrix', 'adjoint_matrix', 'arity']
)


def C(gate):
    """Create a controlled-U gate."""
    return Gate('C{}'.format(gate.name), gate.matrix, gate.adjoint_matrix, 2)


def CC(gate):
    """Create a controlled-controlled-U gate."""
    return Gate('CC{}'.format(gate.name), gate.matrix, gate.adjoint_matrix, 3)
