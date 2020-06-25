
# from . import rst
from . import doks
import argparse
import sys
import traceback


def main():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('source', help=_SOURCE_HELP)
    p.add_argument('target', default=None, nargs='?', help=_TARGET_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    # p.add_argument('--sections', '-s', default=None, help=_SECTIONS_HELP)

    args = p.parse_args()
    try:
        doks.doks(args.source, args.target)
    except Exception as e:
        print(e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        sys.exit(-1)


_DESCRIPTION = """Write a .rst document for a single Python file"""
# _SECTIONS_HELP = 'Characters to use for .rst section headers'
_SOURCE_HELP = '.py file to create documentation for'
_TARGET_HELP = '.rst file to write to.  None means stdout'
_VERBOSE_HELP = """Print more stuff"""


if __name__ == '__main__':
    main()
