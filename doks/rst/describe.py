from . import code
from . import rst
import functools
import inspect

MAX_SIGNATURE = 80


def describe(path, value, sections, is_member, doks):
    section = sections[2 + is_member]

    def describe():
        try:
            dok = doks[value]
        except Exception:
            dok = doks.get(str(path))

        if dok:
            return describe_dok(dok)
        if isinstance(value, functools.partial):
            return describe_partial()
        else:
            return describe_function()

    def describe_dok(dok):
        yield from signature()
        yield ''
        yield dok
        yield ''

    def describe_partial():
        yield from rst.header(path, section)
        yield from ('A partial function:', '')
        yield from rst.code_block('python')
        yield '  functools.partial('
        yield f'      <function {value.func.__name__}>,'
        yield from (f'      {a!r},' for a in value.args)
        yield from (f'      {k}={v!r},' for k, v in value.keywords.items())
        yield from ('  )', '')

    def describe_function():
        doc = inspect.getdoc(value)
        if not (doc and hasattr(value, '__doc__')):
            return

        yield from signature()

        yield code.code(value)
        yield ''

        yield from doc.splitlines()
        yield ''

    def signature():
        if isinstance(value, type):
            line = f'Class ``{path}``'
            yield from rst.header(line, section)
            return

        sig = inspect.signature(value)
        line = f'``{path}{sig}``'

        if len(line) <= MAX_SIGNATURE:
            yield from rst.header(line, section)
        else:
            yield from rst.header(f'``{path}()``', section)
            yield from rst.code_block('python')
            yield f'  {path}('
            for p in sig.parameters.values():
                yield f'       {p},'
            yield from ('  )', '')

    yield from describe()
