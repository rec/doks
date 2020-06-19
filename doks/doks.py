#!/usr/bin/env python3
"""
📚 doks: Automatically create READMEs from your code 📚
====================================================================

Reads the comments from your file and puts them into a servicable .rst
file.

Very suitable for single-file Python libraries that want to keep the code
and documentation in sync without issues

USAGE
-------

.. code-block:: bash

    doks my_file.py [README.rst]

"""
from . import rst
from . import shields
from . import variables
import datetime
import impall
import inspect
import safer

__all__ = ('doks',)


def doks(source, target):
    """Print documentation for a file or module

    ARGUMENTS
      path
        path to the Python file or module.

      target
        path to the output file or ``None``, in which case
        output is printed to stdout

    """
    lines = '\n'.join(_doks(source)) + '\n'
    if not rst.render(lines):
        raise ValueError(f'The .rst code in {source} is malformed')

    with safer.writer(target) as fp:
        fp.write(lines)


def _timestamp():
    return datetime.datetime.now().isoformat()


def _doks(path):
    module = impall.import_file(path)
    module_doc = inspect.getdoc(module) or ''
    def_vars = variables.default_variables(path)

    lines = module_doc.splitlines()
    sections = rst.section_characters(lines)
    yield from shields.add_shields(lines, def_vars)
    yield ''
    yield from rst.header('API', sections[1])

    items = getattr(module, '__all__', vars(module))

    for path, value, is_member in _children(module, items, module.__name__):
        yield from rst.describe(path, value, sections, is_member)

    yield _DOKS_MSG % _timestamp()


def _children(parent, names, module_path, is_member=False):
    for name in names:
        if not name.startswith('_') or name.startswith('__'):
            value = getattr(parent, name)
            if callable(value):
                path = '%s.%s' % (module_path, name)
                yield path, value, is_member

                if isinstance(value, type):
                    yield from _children(value, vars(value), path, True)


_DOKS_URL = 'https://github.com/rec/doks/'
_DOKS_MSG = f'(automatically generated by `doks <{_DOKS_URL}>`_ on %s)'
