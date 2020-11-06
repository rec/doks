from pathlib import Path
import configparser
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
