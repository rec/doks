from unittest import TestCase, mock
import os
from doks import variables

RESULTS = """\
origin	git@ONE.com:TWO/THREE.git (fetch)
origin	git@github.com:rec/doks.git (push)"""

EXPECTED = {
    'bar': 'bing',
    'foo': 'foo',
    'packagename': 'THREE',
    'repo': 'THREE',
    'user': 'TWO',
    'vcsname': 'ONE',
    'vcstype': 'git',
}


class TestVariables(TestCase):
    @mock.patch.dict(os.environ, {'DOKS_FOO': 'foo', 'DOKS_BAR': 'bing'})
    @mock.patch('subprocess.check_output', return_value=RESULTS)
    def test_simple(self, check_output):
        actual = variables.default_variables('.')
        assert EXPECTED == actual

    def test_substitute(self):
        url = 'tests/:user/:repo'
        actual = variables.substitute(EXPECTED, url)
        assert actual == 'tests/TWO/THREE'
