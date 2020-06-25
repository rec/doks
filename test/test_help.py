from pathlib import Path
from readme_renderer import rst
from unittest import TestCase
import io

README_TEXT = (Path(__file__).parents[1] / 'README.rst').read_text()


class TestDoc(TestCase):
    def test_rendering(self):
        out = io.StringIO()
        actual = rst.render(README_TEXT, out)
        if actual is None:
            print('Rendering error!')
            print(out.getvalue())
            assert False
