"""App Utilities functions"""

from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status


def catch_not_implemented_exception(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(self, *args, **kw):
        try:
            return fn(self, *args, **kw)
        except NotImplementedError:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                detail="Method Not Implemented Yet")

    return wrapper


def overrides(interface_class):
    def overrider(method):
        assert (method.__name__ in dir(interface_class))
        return method

    return overrider
