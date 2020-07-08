from doks import doks
from pathlib import Path
from tdir import tdir
from unittest import TestCase, mock
import os

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), 'sample.py')
TIMESTAMP = '2020-05-28T16:26:07.629835'
RESULTS_FILE = Path(__file__).parent / 'test.rst'
EXPECTED = RESULTS_FILE.read_text().splitlines()


class TestDoks(TestCase):
    maxDiff = 100000

    @mock.patch('doks.doks._timestamp', return_value=TIMESTAMP)
    def test_full(self, _timestamp):
        actual = list(doks._doks(SAMPLE_FILE))
        print(*actual, sep='\n')
        assert actual == EXPECTED

    def test_no_change(self):
        with tdir(cwd=False) as td:
            out = td / 'test.rst'
            assert doks.doks(SAMPLE_FILE, out)

            out_lines = out.read_text().splitlines()
            assert out_lines[:-1] == EXPECTED[:-1]

            assert not doks.doks(SAMPLE_FILE, out)
            assert out_lines == out.read_text().splitlines()
