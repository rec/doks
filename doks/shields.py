import yaml
from .extract_shields import FILE

_SHIELD_DATA = {}
_URL_ROOT = 'https://shields.io'


def shield_data():
    if not _SHIELD_DATA:
        with open(FILE) as fp:
            _SHIELD_DATA.update(yaml.safe_load(fp))

    return _SHIELD_DATA


def find_shield(shield_key):
    key, *rest = shield_key.lower().split('.')

    for source, items in shield_data().items():
        if source.lower().startswith(key):
            if not rest:
                return [source] + items[0]
            key, *rest = rest
            for url, name, category in items:
                result = [source, url, name, category]
                if key in url.split('/'):
                    if not rest:
                        return result
                    key, *rest = rest
                    if name.contains(key):
                        if not rest:
                            return result
                        key, = rest
                        if category.startswith(key):
                            return result

    raise ValueError('Bad key ' + shield_key)


def _shield_url(url, source, style, variables):
    parts = url.split('/')
    missing_parts = []
    for i, part in enumerate(parts):
        if part.startswith(':'):
            part = part[1:]
            replacement = variables.get(part)
            if replacement:
                parts[i] = replacement
            else:
                missing_parts.append(part)
    if missing_parts:
        raise ValueError('Missing variables ' + ', '.join(missing_parts))

    base_url = '/'.join([_URL_ROOT, source] + parts)
    if style:
        s = ('%s=%s' % (k, v) for k, v in sorted(style.items()))
        base_url += '?' + '&'.join(s)
    return base_url


def shield_url(key, variables, style=None):
    source, url, name, category = find_shield(key)
    return _shield_url(url, source, style, variables)
