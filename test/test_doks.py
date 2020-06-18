from doks import doks
from pathlib import Path
from unittest import TestCase, mock
import os

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), 'sample.py')
TIMESTAMP = '2020-05-28T16:26:07.629835'


class TestDoks(TestCase):
    maxDiff = 100000

    @mock.patch('doks.doks._timestamp', return_value=TIMESTAMP)
    def test_full(self, _timestamp):
        actual = list(doks._doks(SAMPLE_FILE))
        print(*actual, sep='\n')
        assert actual == EXPECTED


RESULTS_FILE = Path(__file__).parent / 'test.rst'
EXPECTED = RESULTS_FILE.read_text().splitlines()
