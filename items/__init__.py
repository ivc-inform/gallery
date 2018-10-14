def permalink(func):
    """
    Decorator that calls urls.reverse() to return a URL using parameters
    returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
    """
    from functools import wraps
    from django.urls import reverse

    @wraps(func)
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return reverse(bits[0], None, *bits[1:3])

    return inner
