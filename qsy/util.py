import numpy as np


def format_complex(c):
    fmt = '{:+.5f}'.format(c.real).rstrip('0').rstrip('.')

    if not np.isclose(c.imag, 0):
        imag_fmt = '{:+.5f}'.format(c.imag).rstrip('0').rstrip('.') + 'i'
        if np.isclose(c.real, 0.0):
            fmt = imag_fmt
        else:
            fmt += imag_fmt

    return fmt
