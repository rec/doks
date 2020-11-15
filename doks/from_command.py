from .rst import rst
from pathlib import Path
import os
import re
import subprocess

USAGE = 'usage: '


def from_command(path):
    env = dict(os.environ, PYTHONPATH=str(Path('.').absolute()))
    try:
        output = subprocess.check_output((path, '-h'), env=env)
    except Exception:
        output = subprocess.check_output(('python', path, '-h'), env=env)

    lines = output.decode().splitlines()
    yield from _from_command(Path(path).name, lines)


def _arguments(title, *args):
    name = title.split()[0]
    assert name in ('positional', 'optional')
    is_pos = name == 'positional'

    yield from _header('%s arguments' % name.capitalize())
    for i, arg in enumerate(args):
        a = arg.lstrip()
        if not a:
            yield a
            continue
        spaces = len(arg) - len(a)

        if spaces > 4:
            yield '  ' + a
        elif is_pos:
            if i:
                yield ''
            arg, doc = a.split(maxsplit=1)
            yield '``{}``'.format(arg)
            yield '  ' + doc
        else:
            if i:
                yield ''
            flags = []
            doc = []
            in_doc = False

            for part in re.split(r'(\S+)', a):
                if len(part) > 1 and part.isspace():
                    in_doc = True
                else:
                    (doc if in_doc else flags).append(part)

            flags = ''.join(flags).split(',')
            yield ', '.join('``{}``'.format(f.strip()) for f in flags)

            if doc:
                doc[0] = doc[0].capitalize()
                yield '  ' + ''.join(doc)


def _from_command(name, lines):
    usage, desc, pos, opt, *rest = _sections(lines)

    yield from _header(name, 0)

    assert usage[0].startswith(USAGE)
    usage[0] = ' ' * len(USAGE) + usage[0][len(USAGE) :]

    yield from _header('Usage')
    yield from rst.code_block('bash')
    yield from usage

    yield from _header('Description')
    yield from desc

    yield from _arguments(*pos)
    yield from _arguments(*opt)

    if rest:
        (epilog,) = rest
        yield ''
        yield from _header('Comments')
        yield from epilog


def _argument(lines):
    section = []
    for line in lines:
        indent = len(line) - len(line.lstrip())
        if section and indent and indent <= 4:
            yield from section + ['']
            section = []
        section.append(line)

    if section:
        yield from section + ['']


def _sections(lines):
    section = []
    for line in lines:
        if line.strip():
            section.append(line)
        elif section:
            section.append(line)
            yield section
            section = []

    if section:
        yield section


def _header(line, index=1):
    yield from rst.header(line, rst.SECTIONS[index])
