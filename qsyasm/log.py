import sys

NO_COLOR = '\33[m'
BOLD = '\033[1m'
RED, GREEN, ORANGE = ('\33[{}m'.format(i) for i in range(31, 34))


def error_fmt(message):
    return '{}{}error{}: {}'.format(BOLD, RED, NO_COLOR, message)


def warning_fmt(message):
    return '{}{}warning{}: {}'.format(BOLD, ORANGE, NO_COLOR, message)


def info_fmt(message):
    return '{}{}info{}: {}'.format(BOLD, GREEN, NO_COLOR, message)


def print_error(message):
    print(error_fmt(message), file=sys.stderr)


def print_warning(message):
    print(warning_fmt(message), file=sys.stderr)


def print_info(message):
    print(info_fmt(message), file=sys.stderr)
