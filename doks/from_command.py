from . import rst
import subprocess

USAGE = 'usage: '


class State:
    USAGE, DESCRIPTION, ARGS, EPILOG = range(4)


def from_command(path):
    cmd = str(path), '-h'
    try:
        results = subprocess.check_output(cmd)
    except Exception:
        results = subprocess.check_output(('python', *cmd))

    lines = results.decode().splitlines()

    for section in _sections(lines):
        pass


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


def _header(line, index):
    yield from rst.header(line, rst.SECTIONS[index])
