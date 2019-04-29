import argparse
import sys
from .program import QsyASMProgram
from .error import QsyASMError


def main():
    argparser = argparse.ArgumentParser(description='qsyasm assembly runner')

    argparser.add_argument('filename', type=str, help='qsyasm file to execute')
    argparser.add_argument('-t', '--time', action='store_true', help='time program execution')
    argparser.add_argument('-s', '--shots', type=int, default=1, help='amount of shots to run', metavar='N')

    args = vars(argparser.parse_args())

    try:
        p = QsyASMProgram(args)
        p.run()
    except QsyASMError as e:
        print(e, file=sys.stderr)
        sys.exit(-1)
