from doks import rst
from unittest import TestCase


class TestSectionCharacters(TestCase):
    def test_empty(self):
        lines = []
        assert rst.section_characters(lines)[:5] == '-=~_+'

    def test_longer(self):
        assert rst.section_characters(LINES)[:5] == '=#~-_'

    def test_simple(self):
        lines = ['hello', '---', '']
        for i in range(1, 4):
            assert rst.section_characters(lines * i)[:5] == '-=~_+'


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
