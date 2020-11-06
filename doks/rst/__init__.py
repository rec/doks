from pathlib import Path
import configparser
import functools
import inspect
import os

MSG = '`{msg} <https://{host}/{user}/{project}/{sep}/{file}#L{begin}-L{end}>`_'
SEPARATORS = {
    'github.com': 'blob/master',
    'gitlab.com': '-/blob/master',
}
SECTIONS = '-=~_+*#`\':<>^"'

_GIT_SUFFIX = '.git'
_SSH_PREFIX = 'git@'
_HTTPS_PREFIX = 'https://'
ERROR_WINDOW = 10
MAX_SIGNATURE = 80


def describe(path, value, sections, is_member, doks):
    section = sections[2 + is_member]
    if isinstance(value, functools.partial):
        yield from _describe_partial(path, value, section)
    else:
        yield from _describe(path, value, section)


def _describe_partial(path, value, section):
    yield from header(path, section)
    yield from ('A partial function:', '')
    yield from code_block('python')
    yield '  functools.partial('
    yield f'      <function {value.func.__name__}>,'
    yield from (f'      {a!r},' for a in value.args)
    yield from (f'      {k}={v!r},' for k, v in value.keywords.items())
    yield from ('  )', '')


def _describe(path, value, section):
    doc = inspect.getdoc(value)
    if not (doc and hasattr(value, '__doc__')):
        return

    yield from _signature(path, value, section)

    yield code(value)
    yield ''

    yield from doc.splitlines()
    yield ''


def _signature(path, value, section):
    if isinstance(value, type):
        line = f'Class ``{path}``'
        yield from header(line, section)
        return

    sig = inspect.signature(value)
    line = f'``{path}{sig}``'

    if len(line) <= MAX_SIGNATURE:
        yield from header(line, section)
    else:
        yield from header(f'``{path}()``', section)
        yield from code_block('python')
        yield f'  {path}('
        for p in sig.parameters.values():
            yield f'       {p},'
        yield from ('  )', '')


def header(line, char):
    yield from (line, char * len(line), '')


def code_block(lang):
    return f'.. code-block:: {lang}', ''


def code(value):
    while True:
        v = value
        value = getattr(v, '__wrapped__', v)
        if v is value:
            break

    file = os.path.relpath(inspect.getfile(value), '.')

    lines, begin = inspect.getsourcelines(value)
    end = begin + len(lines)
    msg = f'{file}, {begin}-{end}'

    remote = _remote()
    if remote:
        host, user, project = remote
        sep = SEPARATORS[host]
        msg = MSG.format(**locals())

    return f'({msg})'


def section_characters(lines):
    sections = ''
    pline = ''
    for line in lines:
        if line and pline:
            s = line[0]
            if s in SECTIONS and s not in sections and len(set(line)) == 1:
                sections += s
        pline = line

    return ''.join((sections, *(s for s in SECTIONS if s not in sections)))


def _remote():
    git_file = Path('.git/config')
    if not git_file.exists():
        return

    cfg = configparser.ConfigParser()
    cfg.read(git_file)

    remote_urls = (v['url'] for k, v in cfg.items() if k.startswith('remote '))

    suffix = _GIT_SUFFIX
    prefixes = _SSH_PREFIX, _HTTPS_PREFIX

    for remote in remote_urls:
        if remote.endswith(suffix) and remote.count(':') == 1:
            prefix = next((p for p in prefixes if remote.startswith(p)), None)
            if prefix:
                remote = remote[len(prefix) : -len(suffix)]
                parts = remote.replace(':', '/').split('/')
                if len(parts) == 3:
                    if parts[0] in SEPARATORS:
                        return parts
                    else:
                        continue

        raise ValueError('Do not understand remote %s' % remote)
