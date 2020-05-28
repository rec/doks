from .variables import substitute
import os
import shlex
import yaml

_SHIELD_DATA = {}
_URL_ROOT = 'https://img.shields.io'
FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shields.yml')


def shield_data():
    if not _SHIELD_DATA:
        with open(FILE) as fp:
            _SHIELD_DATA.update(yaml.safe_load(fp))

    return _SHIELD_DATA


def _find(shield_key):
    key, *rest = shield_key.lower().split('.')

    for source, items in shield_data().items():
        if not source.lower().startswith(key):
            continue

        if not rest:
            return [source] + items[0]
        k1, *r1 = rest

        for url, alt, category in items:
            result = [source, url, alt, category]
            keys = k1.split('/')

            if k1 and not all(k in url.split('/') for k in keys):
                continue

            if not r1:
                return result
            k2, *r2 = r1
            if k2 not in alt:
                continue

            if not r2:
                return result
            (k3,) = r2
            if category.startswith(k3):
                return result


def find_shield(key):
    shield = _find(key) or _find(key.replace('.', '..', 1))
    if not shield:
        raise ValueError('Bad key ' + key)
    return shield


def _shield_url(key, source, url, style, variables):
    url = url.split('?', maxsplit=1)[0]
    url = substitute(variables, url)

    base_url = '/'.join([_URL_ROOT, source, url])
    if style:
        s = ('%s=%s' % (k, v) for k, v in sorted(style.items()))
        base_url += '?' + '&'.join(s)
    return base_url


def shield_url(key, variables, style=None):
    source, url, alt, category = find_shield(key)
    return _shield_url(key, source, url, style, variables), alt


def parse_shield(key, variables):
    style = None
    if '{' in key:
        sd = yaml.safe_load(key)
        key = sd.pop('key')
        variables = dict(variables, **sd.pop('variables', {}))
        style = sd.pop('style', None)
        if sd:
            raise ValueError('Unknown variables %s' % sd)

    return shield_url(key, variables, style)


PREFIX = '.. doks-shield'


def add_shields(lines, variables):
    shield_lines = []
    in_shield = False
    for line in lines:
        if line.startswith(PREFIX):
            in_shield = True
        elif not in_shield:
            yield line
        elif not line.strip():
            continue
        elif line.startswith(' '):
            shield_lines.append(line)
        else:
            in_shield = False
            shields = shlex.split(' '.join(shield_lines))
            yield ' '.join('|doks_%d|' % i for i in range(len(shields)))
            yield ''
            for i, shield in enumerate(shields):
                url, alt = parse_shield(shield, variables)
                target = url  # FIX
                yield '.. |doks_%d| image:: %s' % (i, url)
                yield '   :alt: ' + alt
                yield '   :target: ' + target
                yield ''

            yield line
