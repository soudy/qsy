import argparse
import sys

from qsy import __version__

from .program import QsyASMProgram
from .error import QsyASMError
from .log import info_message


def main():
    argparser = argparse.ArgumentParser(description='qsyasm assembly runner')

    argparser.add_argument('filename', type=str, help='qsyasm file to execute')
    argparser.add_argument('-V', '--version', action='version',
                           version='%(prog)s v' + __version__)
    argparser.add_argument('-v', '--verbose', action='store_true',
                           help='verbose output')
    argparser.add_argument('-t', '--time', action='store_true',
                           help='time program execution')
    argparser.add_argument('-b', '--backend', choices=('chp', 'statevector'),
                           default=None, metavar='B',
                           help='simulator back-end to use: chp or statevector (default: statevector)')
    argparser.add_argument('-s', '--shots', type=int,
                           default=1, help='amount of shots to run')
    argparser.add_argument('--ignore-print-warning', action='store_true',
                           help='ignore register too large to print warning')

    args = vars(argparser.parse_args())

    try:
        print(info_message('qsyasm v{}'.format(__version__)))
        print(info_message('A state vector/stabilizer circuit simulator assembly runner'))
        print(info_message('=' * 60))

        p = QsyASMProgram(args)
        p.run()
    except QsyASMError as e:
        print(e, file=sys.stderr)
        sys.exit(-1)
