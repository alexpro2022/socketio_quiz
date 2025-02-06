import logging as logger
from collections.abc import Callable
from functools import wraps

from pydantic import ValidationError, validate_call


def validate(
    error_handler: Callable,
    log: bool = True,
    validate_return: bool = False,
    clean_data: Callable | None = None,
    async_mode: bool = True,
) -> Callable[[Callable], Callable]:
    def decor(f):
        SUCCESS_MSG = "Success, result is: {}"
        FAIL_MSG = "Fail, errors are {}"
        EXCEPTIONS = (ValidationError,)
        v_call = validate_call(f, validate_return=validate_return)

        def clean(data):
            return data if clean_data is None else clean_data(data)

        def log_(msg):
            if log:
                logger.info(msg)

        @wraps(f)
        def sync_wrapper(sid, data, *args, **kwargs):
            try:
                res = v_call(sid, clean(data), *args, **kwargs)
                log_(SUCCESS_MSG.format(res))
            except EXCEPTIONS as e:
                res = error_handler(sid, e)
                log_(FAIL_MSG.format(res))
            return res

        @wraps(f)
        async def async_wrapper(sid, data, *args, **kwargs):
            try:
                res = await v_call(sid, clean(data), *args, **kwargs)
                log_(SUCCESS_MSG.format(res))
            except EXCEPTIONS as e:
                res = await error_handler(sid, e)
                log_(FAIL_MSG.format(res))
            return res

        return async_wrapper if async_mode else sync_wrapper

    return decor
