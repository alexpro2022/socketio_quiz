import logging as logger
from asyncio import iscoroutine
from collections.abc import Callable
from functools import wraps

from pydantic import ValidationError, validate_call


def validate(
    error_handler: Callable,
    log: bool = True,
    validate_return: bool = False,
    clean_data: Callable | None = None,
) -> Callable[[Callable], Callable]:
    def decor(f):
        SUCCESS_MSG = "Success, result is: {}"
        FAIL_MSG = "Fail, errors are {}"
        EXCEPTIONS = (ValidationError,)

        def _clean_data(data):
            return data if clean_data is None else clean_data(data)

        def _log(msg):
            if log:
                logger.info(msg)

        @wraps(f)
        def sync_wrapper(sid, data, *args, **kwargs):
            try:
                res = validate_call(f, validate_return=validate_return)(
                    sid, _clean_data(data), *args, **kwargs
                )
                _log(SUCCESS_MSG.format(res))
            except EXCEPTIONS as e:
                res = error_handler(sid, e)
                _log(FAIL_MSG.format(res))
            return res

        @wraps(f)
        async def async_wrapper(sid, data, *args, **kwargs):
            try:
                res = await validate_call(f, validate_return=validate_return)(
                    sid, _clean_data(data), *args, **kwargs
                )
                _log(SUCCESS_MSG.format(res))
            except EXCEPTIONS as e:
                res = await error_handler(sid, e)
                _log(FAIL_MSG.format(res))
            return res

        return async_wrapper
        is_coro = map(iscoroutine, (f, error_handler))
        if all(is_coro):
            return async_wrapper
        elif all(map(lambda x: not x, is_coro)):
            return sync_wrapper
        else:
            raise TypeError(
                f"decorated function {f.__name__} and error_handler"
                f"{error_handler.__name__} types mismatch."
            )

    return decor
