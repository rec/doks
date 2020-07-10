from . import doks
from . import rst
import argparse
import sys
import traceback


def main():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('source', default=None, nargs='?', help=_SOURCE_HELP)
    p.add_argument('target', default=None, nargs='?', help=_TARGET_HELP)
    p.add_argument('--auto', '-a', action='store_true', help=_AUTO_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    p.add_argument(
        '--window', '-w', type=int, default=rst.ERROR_WINDOW, help=_WINDOW_HELP
    )

    args = p.parse_args()
    try:
        doks.doks(**vars(args))
    except Exception as e:
        print(e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        sys.exit(-1)


_DESCRIPTION = """Write a .rst document for a single Python file"""
_SOURCE_HELP = '.py file to create documentation for'
_TARGET_HELP = '.rst file to write to.  None means stdout'
_AUTO_HELP = """Automatically guess which files to read and write"""
_VERBOSE_HELP = """Print more stuff"""
_WINDOW_HELP = """How many lines around an RST error to print
(0 means "print everything")"""


if __name__ == '__main__':
    main()
