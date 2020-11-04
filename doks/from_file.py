from . import rst
from . import shields
import impall
import inspect


def from_file(path):
    m = impall.import_file(str(path))
    module = getattr(m, '_xmod_wrapped', m)
    extends = module is not m and m._xmod_extension

    module_doc = inspect.getdoc(module) or ''

    lines = module_doc.splitlines()
    sections = rst.section_characters(lines)

    yield from shields.add_shields(lines, path)
    yield ''
    yield from rst.header('API', sections[1])

    items = getattr(module, '__all__', None)
    if not items:
        raise ValueError('No items in module')

    if extends:
        yield from rst.describe(path.with_suffix(''), extends, sections, False)

    for vpath, value, is_member in _children(module, items, module.__name__):
        if value is not extends:
            yield from rst.describe(vpath, value, sections, is_member)


def _children(parent, names, module_path, is_member=False):
    for name in names:
        if not name.startswith('_') or name.startswith('__'):
            value = getattr(parent, name)
            if callable(value):
                path = '%s.%s' % (module_path, name)
                yield path, value, is_member

                if isinstance(value, type):
                    yield from _children(value, vars(value), path, True)
