import asyncio
import functools
from infrastructure.config import get_logger


def log_call(func):
    logger = get_logger(func.__module__)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger.debug(f"{func.__name__} called")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"{func.__name__} finished")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger.debug(f"{func.__name__} called")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} finished")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


__all__ = ['log_call']