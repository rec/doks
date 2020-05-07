#!/usr/bin/env python3
"""
``doks``

"""
import impall
import importlib
import inspect
import os
import sys

__all__ = 'doks',


def doks(path):
    """Print documentation for a file or module

    ARGUMENTS
      path: path to the Python file or module.
    """

    root, module_path = impall.import_path(path)
    root and os.chdir(root)
    module = importlib.import_module(module_path)
    for line in _get_doc(module):
        print(line)

    items = {k: getattr(module, k) for k in module.__all__}
    _print_all(items, module_path, '')


def _print_all(items, module, indent):
    def print_lines(*lines):
        for i in lines:
            print(indent + i if i.strip() else i)

    def print_name(name):
        print_lines('``%s``' % name)

    for k, v in items.items():
        if callable(v) and (not k.startswith('_') or k.startswith('__')):
            name = '%s.%s' % (module, k)
            if _is_type(v):
                print_name(name)
                _print_all(vars(v), name, indent + '    ')
            else:
                print_name(name + str(inspect.signature(v)))
                print_lines(*_get_doc(v))


def _is_type(value):
    while True:
        wrapped = getattr(value, '__wrapped__', None)
        if not wrapped:
            return isinstance(value, type)
        value = wrapped


def _get_doc(s):
    lines = (s.__doc__ or '').splitlines()
    prefix = os.path.commonprefix(lines)
    blanks = len(prefix) - len(prefix.lstrip())
    return [i[blanks:] for i in lines]


if __name__ == '__main__':
    doks(sys.argv[1])
