from doks import from_command
from pathlib import Path
from unittest import TestCase

DOKS_HELP = Path(__file__).parent / 'doks-help.txt'
DOKS_OUTPUT = DOKS_HELP.read_text().splitlines()
DOKS_RESULTS = Path(__file__).parent / 'doks-results.rst'

ARGUMENTS = Path(__file__).parent / 'arguments.txt'


class TestArguments(TestCase):
    def test_arguments(self):
        args = DOKS_OUTPUT[-8:]
        assert args[0] == 'optional arguments:'

        actual = list(from_command._argument(args))
        expected = ARGUMENTS.read_text().splitlines() + ['']
        assert actual == expected


class TestSections(TestCase):
    def test_sections(self):
        actual = list(from_command._sections(DOKS_OUTPUT))
        assert actual == EXPECTED_SECTIONS


class TestFromCommand(TestCase):
    def test_from_command(self):
        actual = list(from_command._from_command('doks', DOKS_OUTPUT))
        expected = DOKS_RESULTS.read_text().splitlines()
        assert actual == expected


EXPECTED_SECTIONS = [
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
