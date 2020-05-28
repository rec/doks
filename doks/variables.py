import os
import re
import subprocess

ENV_PREFIX = 'DOKS_'
DEFAULTS = {'vcstype': 'github'}
FILL_INS = (('packagename', 'repo'),)
SUB = {'stderr': subprocess.DEVNULL, 'encoding': 'utf8'}


def remotes(path):
    cmd = 'git', 'remote', '-v'
    cwd = (path if os.path.isdir(path) else os.path.dirname(path)) or None

    try:
        out = subprocess.check_output(cmd, cwd=cwd, **SUB)
    except Exception:
        return {}

    search = re.compile(r'\bgit@(\w+)\.\w+:(\w+)/(\w+)\.git\b').search
    for remote in out.splitlines():
        match = search(remote)
        if match:
            vcsname, user, repo = match.groups()
            return {'vcsname': vcsname, 'user': user, 'repo': repo}

    return {}


def fill_in(variables, subs=FILL_INS):
    for missing, sub in subs:
        if missing not in variables:
            try:
                variables[missing] = variables[sub]
            except KeyError:
                pass


def env_variables():
    e = {k: v for k, v in os.environ.items() if k.startswith(ENV_PREFIX)}
    p = len(ENV_PREFIX)
    return {k[p:].lower(): v for k, v in e.items()}


def substitute(variables, url):
    parts = url.split('/')
    missing_parts = []
    new_parts = []
    for part in parts:
        if part.startswith(':'):
            optional = part.endswith('*')
            part = part[1:-1] if optional else part[1:]
            replacement = variables.get(part.lower())
            if replacement:
                new_parts.append(replacement)
            elif not optional:
                missing_parts.append(part)
        else:
            new_parts.append(part)

    if missing_parts:
        parts = ', '.join(missing_parts)
        print(variables)
        raise ValueError('Missing variables %s in %s' % (parts, url))

    return '/'.join(new_parts)


def default_variables(path):
    v = dict(DEFAULTS)
    v.update(remotes(path))
    v.update(env_variables())
    fill_in(v)
    return v


def substitutor(path):
    dv = default_variables(path)

    return lambda url: substitute(dv, url)
