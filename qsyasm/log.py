NO_COLOR = '\33[m'
BOLD = '\033[1m'
RED, GREEN, ORANGE = ('\33[{}m'.format(i) for i in range(31, 34))

def error_message(message):
    return '{}{}error{}: {}'.format(BOLD, RED, NO_COLOR, message)

def warning_message(message):
    return '{}{}warning{}: {}'.format(BOLD, ORANGE, NO_COLOR, message)

def info_message(message):
    return '{}{}info{}: {}'.format(BOLD, GREEN, NO_COLOR, message)
