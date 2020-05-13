from doks import shields
import unittest


class TestFindShields(unittest.TestCase):
    def test_empty(self):
        expected = [
            ':tenant.myget',
            ':feed/dt/:packageName',
            'MyGet tenant',
            'downloads',
        ]
        actual = shields.find_shield('')
        assert actual == expected

    def test_github1(self):
        actual = shields.find_shield('github')
        expected = [
            'github',
            ':issueKind/detail/:property/:user/:repo/:number',
            'GitHub issue/pull request detail',
            'issue-tracking',
        ]
        assert actual == expected

    def test_github2(self):
        actual = shields.find_shield('github.last-commit')
        expected = [
            'github',
            'last-commit/:user/:repo',
            'GitHub last commit',
            'activity',
        ]
        assert actual == expected

    def test_github3(self):
        actual = shields.find_shield('github.release')
        expected = [
            'github',
            'v/release/:user/:repo',
            'GitHub release (latest by date)',
            'version',
        ]
        assert actual == expected

    def test_travis(self):
        actual = shields.find_shield('travis')
        expected = ['travis', ':user/:repo', 'Travis (.org)', 'build']
        assert actual == expected


class TestShieldURL(unittest.TestCase):
    def test_github2(self):
        actual = shields.shield_url(
            'github.last-commit', user='rec', repo='doks'
        )
        expected = 'https://shields.io/github/last-commit/rec/doks'
        assert actual == expected

    def test_travis(self):
        actual = shields.shield_url('travis', user='rec', repo='doks')
        expected = 'https://shields.io/travis/rec/doks'
        assert actual == expected

    def test_travis2(self):
        style = {'color': 'FF00FF', 'label': 'blah', 'style': 'plastic'}
        actual = shields.shield_url('travis', style, user='rec', repo='doks')
        expected = (
            'https://shields.io/travis/rec/doks'
            '?color=FF00FF&label=blah&style=plastic'
        )
        assert actual == expected
