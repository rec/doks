from doks import variables
from unittest import TestCase, mock
import os

RESULTS = """\
origin	git@ONE.com:TWO/THREE.git (fetch)
origin	git@github.com:rec/doks.git (push)

# comment

"""

EXPECTED = {
    'bar': 'bing',
    'foo': 'foo',
    'packagename': 'THREE',
    'repo': 'THREE',
    'user': 'TWO',
    'vcsname': 'ONE',
    'vcstype': 'github',
}


@mock.patch.dict(os.environ, {'DOKS_FOO': 'foo', 'DOKS_BAR': 'bing'})
@mock.patch('subprocess.check_output', return_value=RESULTS)
class TestVariables(TestCase):
    def test_simple(self, check_output):
        actual = variables.default_variables('.')
        assert EXPECTED == actual

    def test_substitute(self, check_output):
        sub = variables.substitutor('.')
        actual = sub('tests/:user/:repo')
        assert actual == 'tests/TWO/THREE'

    def test_missing(self, check_output):
        sub = variables.substitutor('.')
        with self.assertRaises(ValueError) as m:
            sub('tests/:user/:repong')
        expected = 'Missing variables repong in tests/:user/:repong'
        actual = m.exception.args[0]
        assert actual == expected

    def test_optional(self, check_output):
        sub = variables.substitutor('.')
        actual = sub('grade/:vcsType/:user/:repo/:branch*')
        expected = 'grade/github/TWO/THREE'
        assert actual == expected
