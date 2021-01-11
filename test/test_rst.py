from doks.rst import rst
from unittest import TestCase


class TestSectionCharacters(TestCase):
    def test_empty(self):
        lines = []
        assert rst.section_characters(lines)[:5] == '-=~_+'

    def test_longer(self):
        assert rst.section_characters(LINES)[:5] == '=#~-_'

    def test_ticks(self):
        assert rst.fix_ticks(TICKS) == TICKS_FIXED

    def test_simple(self):
        lines = ['hello', '---', '']
        for i in range(1, 4):
            assert rst.section_characters(lines * i)[:5] == '-=~_+'


TICKS = """
Use `pip <https://pypi.org/project/pip>`_ to install `safer` from the command
line: `pip install safer`.

Tested on Python 3.4 - 3.9.  An old Python 2.7 version
is `here <https://github.com/rec/safer/tree/v2.0.5>`_.
"""

TICKS_FIXED = """
Use `pip <https://pypi.org/project/pip>`_ to install ``safer`` from the command
line: ``pip install safer``.

Tested on Python 3.4 - 3.9.  An old Python 2.7 version
is `here <https://github.com/rec/safer/tree/v2.0.5>`_.
"""

LINES = """
First
======

Second
#######

--------

FIRST!
=======

Second!
#########

Third
~~~~~~

""".splitlines()
