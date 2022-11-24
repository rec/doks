from pathlib import Path
from . import shields
from .rst.describe import describe
from .rst import rst
import impall
import inspect

INIT = '/__init__.py'


def from_file(path):
    if isinstance(path, Path):
        p = str(path)
    else:
        p, path = path, Path(path)
    if p.endswith(INIT):
        p = p[:-len(INIT)]

    m = impall.import_file(p)
    doks = getattr(m, '_DOKS', {})
    try:
        module = m._xmod_wrapped
    except AttributeError:
        module = m
        extends = None
    else:
        extends = m._xmod_extension

    module_doc = rst.fix_ticks(inspect.getdoc(module) or '')

    lines = module_doc.splitlines()
    sections = rst.section_characters(lines)

    yield from shields.add_shields(lines, path)
    yield ''
    yield from rst.header('API', sections[1])

    items = getattr(module, '__all__', None)
    if not items:
        raise ValueError('No items in module')

    if extends:
        d = path.with_suffix('')
        yield from describe(d, extends, sections, False, doks)

    for vpath, value, is_member in _children(module, items, module.__name__):
        if value is not extends:
            yield from describe(vpath, value, sections, is_member, doks)


def _children(parent, names, module_path, is_member=False):
    module_path = module_path.replace('.__init__', '')
    for name in names:
        if not name.startswith('_') or name.startswith('__'):
            value = getattr(parent, name)
            if callable(value):
                path = '%s.%s' % (module_path, name)
                yield path, value, is_member

                if isinstance(value, type):
                    yield from _children(value, vars(value), path, True)
