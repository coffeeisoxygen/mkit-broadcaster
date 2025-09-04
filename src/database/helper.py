from collections.abc import Awaitable, Callable
from typing import TypeVar

from database import sessionmanager

T = TypeVar("T")


async def run_in_session[T](func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
    """Run a coroutine function within a database session.

    Parameters
    ----------
    func : Callable
        An async function that accepts a database session as its first argument.
    *args, **kwargs :
        Arguments to pass to the function.

    Returns:
    -------
    Any
        The result of the function.
    """
    async with sessionmanager.session() as db:
        return await func(db, *args, **kwargs)
