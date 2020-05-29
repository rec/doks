"""Top level docs"""


def function(a, b, c='hello', **kwargs):
    """"This is function()."""


class Class(str):
    """Here's class"""

    def __init__(self, *args, **kwargs):
        """a constructor"""
        super().__init__(*args, **kwargs)

    def public(self, foo, bar, baz):
        """
        A public method.

        ARGUMENTS:
          foo
            a foo

          bar
            a bar

          baz
            no idea
        """

    def undocumented(self, foo, bar, baz):
        pass

    def _protected(self, foo, bar, baz):
        """You shouldn't see this."""