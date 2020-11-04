from . import doks
from pathlib import Path
import argparse
import sys
import toml
import traceback

PYP = Path('pyproject.toml')


def main():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('source', default=None, nargs='?', help=_SOURCE_HELP)
    p.add_argument('target', default=None, nargs='?', help=_TARGET_HELP)
    p.add_argument('--auto', '-a', action='store_true', help=_AUTO_HELP)
    p.add_argument('--command', '-c', action='store_true', help=_COMMAND_HELP)
    p.add_argument('--force', '-f', action='store_true', help=_FORCE_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    p.add_argument('--window', '-w', help=_WINDOW_HELP)

    args = vars(p.parse_args())

    if PYP.exists():
        project = toml.load(PYP.open())
        project = project.get('tool', {}).get('doks', {})
    else:
        project = {}

    bad_project = set(project) - set(args)
    if bad_project:
        bp = sorted(bad_project)
        print('Do not understand values in', PYP, ':', *bp, file=sys.stderr)
        project = {k: v for k, v in project.items() if k in args}

    for k, v in args.items():
        if not (k in project or v in (False, None)):
            project[k] = v

    try:
        doks.doks(**project)
    except Exception as e:
        print(e, file=sys.stderr)
        if args.get('verbose'):
            traceback.print_exc()
        sys.exit(-1)


_DESCRIPTION = """Write a .rst document for a single Python file"""
_SOURCE_HELP = '.py file to create documentation for'
_TARGET_HELP = '.rst file to write to.  None means stdout'
_AUTO_HELP = """Automatically guess which files to read and write"""
_COMMAND_HELP = """Use command line help from executing source instead"""
_FORCE_HELP = """Write .rst documentation even if it is malformed"""
_VERBOSE_HELP = """Print more stuff"""
_WINDOW_HELP = """How many lines around an RST error to print
(0 means "print everything")"""


if __name__ == '__main__':
    main()
