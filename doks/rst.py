from pathlib import Path
from readme_renderer import rst
import inspect
import io
import os
import configparser
import sys

USE_INDENT = False

MSG = '`{msg} <https://{host}/{user}/{project}/{sep}/{file}#L{begin}-L{end}>`_'
SEPARATORS = {
    'github.com': 'blob/master',
    'gitlab.com': '-/blob/master',
}
SECTIONS = '-=~_+*#`\':<>^"'

_GIT_SUFFIX = '.git'
_SSH_PREFIX = 'git@'
_HTTPS_PREFIX = 'https://'


def render(text):
    out = io.StringIO()

    rendered = rst.render(text, out)
    if not rendered:
        print('.rst Rendering error!', file=sys.stderr)
        print(out.getvalue(), file=sys.stderr)
        print('', file=sys.stderr)

        lines = text.splitlines()
        fmt = '%0{}d:'.format(len(str(1 + len(lines))))
        for i, line in enumerate(lines):
            print(fmt % (i + 1), line, file=sys.stderr)

    return rendered


def describe(path, value, sections):
    if isinstance(value, type):
        yield from header(f'Class `{path}``', sections[2])
    else:
        sig = inspect.signature(value)
        yield from header(f'``{path}{sig}``', sections[3])

    yield code(value)
    yield ''

    doc = inspect.getdoc(value)
    if doc:
        yield from indent(doc)
    yield ''


def header(line, char):
    yield from (line, char * len(line), '')


def code(value):
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


def indent(s):
    for line in s.splitlines():
        if USE_INDENT:
            yield '    ' + line if line.strip() else line
        else:
            yield line


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