"""Top level docs"""

__all__ = 'function', 'Class'


def function(a, b, c='hello', **kwargs):
    """This is a function()."""


class Class:
    "This is a class"

    def __init__(self, *args, **kwargs):
        """a constructor"""
        self.args = args
        self.kwargs = kwargs

    # """before public"""
    def public(self, foo, bar, baz):
        """
        A public method.

        ARGUMENTS
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
