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
from pathlib import Path
import datetime
import impall
import inspect
import safer

__all__ = ('doks',)


def doks(source, target, auto=False):
    """Print documentation for a file or module

    ARGUMENTS
      source
        path to the Python file or module.

      target
        path to the output file or ``None``, in which case
        output is printed to stdout

      auto
        If true, automatically guess both source and target files

    """
    if source and auto:
        raise ValueError('Source cannot be set if --auto/-a is used')

    if not (source or auto):
        raise ValueError('Source must be set if --auto/-a is not used')

    if auto:
        source = _auto_source()
        target = 'README.rst'

    lines = list(_doks(source))
    body = '\n'.join(lines) + '\n'
    if not rst.render(body):
        raise ValueError(f'The .rst code in {source} is malformed')

    p = Path(target)
    if p.exists() and p.read_text().splitlines()[:-1] == lines[:-1]:
        print(f'{target} unchanged')
        return

    with safer.writer(target) as fp:
        fp.write(body)

    written = 'rewritten' if p.exists() else 'written'
    print(f'{target} {written}')
    return True


def _auto_source():
    eponymous = Path(Path().absolute().stem + '.py')
    if eponymous.exists():
        return eponymous

    def accept(p):
        if p.suffix == '.py' and p.name != 'setup.py':
            return not (p.name.startswith('test') or p.name.startswith('.'))

    files = sorted(p for p in Path().iterdir() if accept(p))
    if not files:
        raise ValueError('No Python files to document')
    if len(files) > 1:
        files = ', '.join(str(f) for f in files)
        raise ValueError(f'Too many possible Python files: {files}')
    return files[0]


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

    items = getattr(module, '__all__', None)
    if not items:
        raise ValueError('No items in module')

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
