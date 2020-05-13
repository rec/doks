from doks import shields
import unittest


class TestFindShields(unittest.TestCase):
    def test_empty(self):
        expected = [
            ':tenant.myget',
            'MyGet tenant',
            ':feed/dt/:packageName',
            'downloads',
        ]
        actual = shields.find_shield('')
        assert actual == expected

    def test_github1(self):
        actual = shields.find_shield('github')
        expected = ['github', 'GitHub', 'license/:user/:repo', 'license']
        assert actual == expected

    def test_github2(self):
        actual = shields.find_shield('github.last-commit')
        expected = [
            'github',
            'GitHub last commit',
            'last-commit/:user/:repo',
            'activity',
        ]
        assert actual == expected

    def test_github3(self):
        actual = shields.find_shield('github.release')
        expected = [
            'github',
            'GitHub release (latest SemVer including pre-releases)',
            'v/release/:user/:repo?include_prereleases&sort=semver',
            'version',
        ]
        assert actual == expected

    def test_github4(self):
        actual = shields.find_shield('github.languages/top')
        expected = [
            'github',
            'GitHub top language',
            'languages/top/:user/:repo',
            'analysis',
        ]
        assert actual == expected

    def test_travis(self):
        actual = shields.find_shield('travis..org')
        expected = ['travis', 'Travis (.org)', ':user/:repo', 'build']
        assert actual == expected


_VARS = {
    'user': 'rec',
    'repo': 'doks',
    'vcsType': 'git',
    'vcsName': 'github',
    'packageName': 'doks',
}
_STYLE = {'color': 'FF00FF', 'label': 'blah', 'style': 'plastic'}


class TestShieldURL(unittest.TestCase):
    def test_github2(self):
        actual = shields.shield_url('github.last-commit', _VARS)
        expected = 'https://shields.io/github/last-commit/rec/doks'
        assert actual == (expected, 'GitHub last commit')

    def test_travis(self):
        actual = shields.shield_url('travis..org', _VARS)
        expected = ('https://shields.io/travis/rec/doks', 'Travis (.org)')
        assert actual == expected

    def test_travis2(self):
        actual = shields.shield_url('travis..org', _VARS, _STYLE)[0]
        expected = (
            'https://shields.io/travis/rec/doks'
            '?color=FF00FF&label=blah&style=plastic'
        )
        assert actual == expected


class TestAddShields(unittest.TestCase):
    def test_add(self):
        actual = '\n'.join(shields.add_shields(LINES.splitlines(), _VARS))
        print(actual)
        assert actual == EXPECTED


LINES = """
-------------------------------
✏️safer: a safer file opener ✏️
-------------------------------

.. doks-shields::

   travis..org codecov github.release pypi.pyversions github.top/languages
   codefactor pypi.l github.code-size

No more partial writes or corruption! For file streams, sockets or
any callable.
"""

EXPECTED = """
-------------------------------
✏️safer: a safer file opener ✏️
-------------------------------

.. image:: https://shields.io/travis/rec/doks
   :alt: Travis (.org)

.. image:: https://shields.io/codecov/c/github/rec/doks
   :alt: Codecov

.. image:: https://shields.io/github/v/release/rec/doks
   :alt: GitHub release (latest SemVer including pre-releases)

.. image:: https://shields.io/pypi/pyversions/doks
   :alt: PyPI - Python Version

.. image:: https://shields.io/github/languages/top/rec/doks
   :alt: GitHub top language

.. image:: https://shields.io/codefactor/grade/git/rec/doks/:branch*
   :alt: CodeFactor Grade

.. image:: https://shields.io/pypi/l/doks
   :alt: PyPI - License

.. image:: https://shields.io/github/languages/code-size/rec/doks
   :alt: GitHub code size in bytes

No more partial writes or corruption! For file streams, sockets or
any callable."""
