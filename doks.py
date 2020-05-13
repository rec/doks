#!/usr/bin/env python3
"""
``doks``

"""
import datetime
import impall
import inspect
import os
import sys

__all__ = 'Test', 'doks',


class Test:
    """Test is great!"""

    def __init__(self, foo, bar):
        """Test Dox here!!"""
        pass

    def _foo(self):
        pass

    def __bool__(self):
        pass


def doks(path):
    """Print documentation for a file or module

    ARGUMENTS
      path: path to the Python file or module.
    """
    def indent(lines):
        for line in lines:
            if line.strip():
                print('    ', end='')
            print(line)

    def header(line, char='-'):
        header = char * len(line)
        if char in '*#':
            print(header)
        print(line)
        print(header)
        print()

    def get_doc(s):
        lines = (s.__doc__ or '').splitlines()
        while lines and not lines[-1].strip():
            lines.pop()

        while lines and not lines[0].strip():
            lines.pop(0)

        prefix = os.path.commonprefix(lines)
        blanks = len(prefix) - len(prefix.lstrip())
        return [i[blanks:] for i in lines]

    def print_children(parent, names, module_path):
        for name in names:
            if not name.startswith('_') or name.startswith('__'):
                value = getattr(parent, name)
                new_path = '%s.%s' % (module_path, name)
                if isinstance(value, type):
                    header('Class ``%s``' % new_path, '=')
                    indent(get_doc(value))
                    print()
                    print_children(value, vars(value), new_path)

                elif callable(value):
                    sig = str(inspect.signature(value))
                    header('``%s%s``' % (new_path, sig))
                    indent(get_doc(value))
                    print()

    module = impall.import_file(path)
    for line in get_doc(module):
        print(line)
    print()
    header('API', '*')
    print_children(module, module.__all__, module.__name__)

    timestamp = datetime.datetime.now().isoformat()
    print('automatically generated by doks on %s' % timestamp)


if __name__ == '__main__':
    doks(sys.argv[1])
