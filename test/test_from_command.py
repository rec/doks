from doks import from_command
from unittest import TestCase


class TestFromCommand(TestCase):
    def test_sections(self):
        actual = [i for i in from_command._sections(SECTIONS)]
        assert actual == EXPECTED


EXPECTED = [
    [
        'usage: doks [-h] [--auto] [--command] [--verbose] [--window WINDOW]',
        '            [source] [target]',
        '',
    ],
    ['Write a .rst document for a single Python file', ''],
    [
        'positional arguments:',
        '  source                .py file to create documentation for',
        '  target                .rst file to write to. None means stdout',
        '',
    ],
    [
        'optional arguments:',
        '  -h, --help            show this help message and exit',
        '  --auto, -a            '
        'Automatically guess which files to read and write',
        '  --command, -c         '
        'Use command line help from executing source instead',
        '  --verbose, -v         Print more stuff',
        '  --window WINDOW, -w WINDOW',
        '                        '
        'How many lines around an RST error to print (0 means',
        '                        "print everything")',
    ],
]


SECTIONS = """

usage: doks [-h] [--auto] [--command] [--verbose] [--window WINDOW]
            [source] [target]


Write a .rst document for a single Python file


positional arguments:
  source                .py file to create documentation for
  target                .rst file to write to. None means stdout

optional arguments:
  -h, --help            show this help message and exit
  --auto, -a            Automatically guess which files to read and write
  --command, -c         Use command line help from executing source instead
  --verbose, -v         Print more stuff
  --window WINDOW, -w WINDOW
                        How many lines around an RST error to print (0 means
                        "print everything")
""".splitlines()
