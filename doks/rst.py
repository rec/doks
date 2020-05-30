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


def describe(path, value):
    if isinstance(value, type):
        head = f'Class `{path}``'
        char = '='
    else:
        sig = inspect.signature(value)
        head = f'``{path}{sig}``'
        char = '-'
    yield from header(head, char)
    yield code(value)
    yield ''

    doc = inspect.getdoc(value)
    if doc:
        yield from indent(doc)
    yield ''


def header(line, char='-'):
    header = char * len(line)
    if char in '#':
        yield header
    yield from (line, header, '')


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
