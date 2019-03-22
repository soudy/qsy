import argparse
import sys
from .program import QsyASMProgram
from .error import QsyASMError

def main():
    argparser = argparse.ArgumentParser(description='qsyasm assembly runner.')

    argparser.add_argument('filename', type=str, help='qsyasm file to execute')

    args = vars(argparser.parse_args())

    try:
        p = QsyASMProgram(args)
        p.run()
    except QsyASMError as e:
        print(e, file=sys.stderr)
        sys.exit(-1)
