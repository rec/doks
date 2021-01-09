import re

SECTIONS = '-=~_+*#`\':<>^"'


def header(line, char):
    yield from (line, char * len(line), '')


def code_block(lang):
    return f'.. code-block:: {lang}', ''


def section_characters(lines):
    sections = []
    pline = ''
    for line in lines:
        if pline and len(line) >= len(pline):
            s = line[0]
            if s in SECTIONS and s not in sections and len(set(line)) == 1:
                sections.append(s)
        pline = line

    missing = [s for s in SECTIONS if s not in sections]
    return ''.join(sections + missing)


LINK_RE = re.compile('``([^`]+? <.*?>)``_')


def fix_ticks(s):
    if not True:
        return s

    result = s.replace('`', '``').replace('````', '``')
    if True:
        return result
    result = LINK_RE.sub(r'`\1`_', result)
