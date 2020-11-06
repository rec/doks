from readme_renderer import rst
import io
import sys

ERROR_WINDOW = 10


def render(text, window=ERROR_WINDOW):
    out = io.StringIO()

    rendered = rst.render(text, out)
    if rendered:
        return rendered

    print('.rst Rendering error!', file=sys.stderr)
    error = out.getvalue()
    try:
        error_line = int(error.split(':')[1])
    except Exception:
        error_line = -1

    print(error, file=sys.stderr)
    print('', file=sys.stderr)

    lines = text.splitlines()
    fmt = '%0{}d:'.format(len(str(1 + len(lines))))

    half_win = (window + 1) // 2
    for i, line in enumerate(lines):
        if error_line is None or not window or abs(i - error_line) <= half_win:
            symbol = '->' if i == error_line - 1 else '  '
            print(symbol, fmt % (i + 1), line, file=sys.stderr)
