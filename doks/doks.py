#!/usr/bin/env python3
"""
``doks``

"""
from . import shields
from . import variables
import datetime
import impall
import inspect
import os
import safer
import sys

__all__ = ('doks',)


def _doks(path, print=print):
    """Print documentation for a file or module

    ARGUMENTS
      path: path to the Python file or module.
    """

    def indent(lines):
        for line in lines:
            if line.strip():
                line = '    ' + line
            print(line)

    def header(line, char='-'):
        header = char * len(line)
        if char in '*#':
            print(header)
        print(line)
        print(header)
        print()

    def print_children(parent, names, module_path):
        for name in names:
            if not name.startswith('_') or name.startswith('__'):
                value = getattr(parent, name)
                new_path = '%s.%s' % (module_path, name)

                if isinstance(value, type):
                    header('Class ``%s``' % new_path, '=')
                    indent(_get_doc(value))
                    print()
                    print_children(value, vars(value), new_path)

                elif callable(value):
                    sig = str(inspect.signature(value))
                    header('``%s%s``' % (new_path, sig))
                    indent(_get_doc(value))
                    print()

    module = impall.import_file(path)
    module_doc = _get_doc(module)

    def_vars = variables.default_variables(path)
    for line in shields.add_shields(module_doc, def_vars):
        print(line)
    print()
    header('API', '*')
    print_children(module, module.__all__, module.__name__)

    timestamp = datetime.datetime.now().isoformat()
    print('(automatically generated by doks on %s)' % timestamp)


def _get_doc(s):
    lines = (s.__doc__ or '').splitlines()
    while lines and not lines[-1].strip():
        lines.pop()

    while lines and not lines[0].strip():
        lines.pop(0)

    prefix = os.path.commonprefix([i for i in lines if i.strip()])
    blanks = len(prefix) - len(prefix.lstrip())
    return [i[blanks:] for i in lines]


def doks(source, target=None):
    if target:
        with safer.printer(target) as print:
            _doks(source, print)
    else:
        _doks(source)


def main():
    doks(*sys.argv[1:])


if __name__ == '__main__':
    main()
