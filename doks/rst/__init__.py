SECTIONS = '-=~_+*#`\':<>^"'
ERROR_WINDOW = 10


def header(line, char):
    yield from (line, char * len(line), '')


def code_block(lang):
    return f'.. code-block:: {lang}', ''


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
