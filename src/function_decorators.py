"""
A central place to keep all function decorators
"""


def static(name, val):
    """Creates static attributes for a function"""
    def decorate(func):
        setattr(func, name, val)
        return func
    return decorate
