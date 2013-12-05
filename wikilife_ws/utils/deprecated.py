# coding=utf-8


class Deprecated():
    """
    Add this decorator to deprecated classes.
    ``date`` should be the date since it was deprecated (this will be included in the generated docs)
    """

    def __init__(self, date):
        self._deprecated_since = date

    def __call__(self, clazz):
        clazz._deprecated_since = self._deprecated_since
        return clazz
