import subprocess


class State:
    USAGE, DESCRIPTION, ARGS, EPILOG = range(4)


def from_command(path):
    try:
        results = subprocess.check_output((str(path), '-h'))
    except Exception:
        results = subprocess.check_output('python', (str(path), '-h'))

    state = State.USAGE
    return results, state
