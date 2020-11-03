from doks import doks
from doks.from_file import from_file
from pathlib import Path
from unittest import TestCase, mock
import os
import tdir

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), 'sample.py')
TIMESTAMP = '2020-05-28T16:26:07.629835'
RESULTS_FILE = Path(__file__).parent / 'test.rst'
EXPECTED = RESULTS_FILE.read_text().splitlines()[:-1]


class TestDoks(TestCase):
    maxDiff = 100000

    @mock.patch('doks.doks._timestamp', return_value=TIMESTAMP)
    def test_full(self, _timestamp):
        actual = list(from_file(SAMPLE_FILE))
        print(*actual, sep='\n')
        assert actual == EXPECTED

    def test_no_change(self):
        with tdir(chdir=False) as td:
            out = td / 'test.rst'
            assert doks.doks(SAMPLE_FILE, out)

            out_lines = out.read_text().splitlines()
            assert out_lines[:-1] == EXPECTED

            assert not doks.doks(SAMPLE_FILE, out)
            assert out_lines == out.read_text().splitlines()

    @tdir('setup.py', 'test.py', 'result.py')
    def test_auto1(self):
        assert doks._guess_source() == Path('result.py')

    @tdir(fancy=('fancy.py', 'test.py', 'foo.py'))
    def test_auto2(self):
        os.chdir('fancy')
        assert doks._guess_source() == Path('fancy.py')

    @tdir(fancy=('funny.py', 'test.py', 'foo.py'))
    def test_auto3(self):
        os.chdir('fancy')
        with self.assertRaises(ValueError) as m:
            doks._guess_source()
        expected = 'Too many possible Python files: foo.py, funny.py'
        assert m.exception.args[0] == expected

    @tdir('test_all.py', 'test_none.py', 'setup.py')
    def test_auto4(self):
        with self.assertRaises(ValueError) as m:
            doks._guess_source()
        assert m.exception.args[0] == 'No Python files to document'
