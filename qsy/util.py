import numpy as np


def format_complex(c):
    c = c if not np.isclose(c, 0.0) else 0.0
    format = '{:+.5f}'.format(c.real).rstrip('0').rstrip('.')

    if not np.isclose(c.imag, 0):
        if np.isclose(c.real, 0.0):
            format = '{:+.5f}'.format(c.imag).rstrip('0').rstrip('.') + 'i'
        else:
            format += ' {:+.5f}'.format(c.imag).rstrip('0').rstrip('.') + 'i'

    return format
