from doks import from_command
from pathlib import Path
from unittest import TestCase

RESULT_FILE = Path(__file__).parent / 'results.rst'
HELP_FILE = Path(__file__).parent / 'help-output.txt'
ARGUMENTS = Path(__file__).parent / 'arguments.txt'

HELP_OUTPUT = HELP_FILE.read_text().splitlines()


class TestArguments(TestCase):
    def test_arguments(self):
        args = HELP_OUTPUT[-8:]
        assert args[0] == 'optional arguments:'

        actual = list(from_command._argument(args))
        expected = ARGUMENTS.read_text().splitlines() + ['']
        assert actual == expected


class TestSections(TestCase):
    def test_sections(self):
        actual = list(from_command._sections(HELP_OUTPUT))
        assert actual == EXPECTED_SECTIONS


class TestFromCommand(TestCase):
    def test_from_command(self):
        actual = list(from_command._from_command('doks', HELP_OUTPUT))
        expected = RESULT_FILE.read_text().splitlines()
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
