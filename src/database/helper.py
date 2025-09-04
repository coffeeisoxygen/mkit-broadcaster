"""Helper utilities for database session management.

This module provides functions to simplify running async database operations
without manually passing session objects. It is intended to make database
access more convenient and consistent across the codebase.
"""

from collections.abc import Awaitable, Callable
from typing import TypeVar

from database import sessionmanager

T = TypeVar("T")


async def run_in_session[T](func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
    """Run a coroutine function within a managed database session.

    This function automatically creates a database session, passes it as the
    first argument to the provided async function, and ensures proper cleanup.

    Args:
        func (Callable[..., Awaitable[T]]): An async function that expects a
            database session as its first argument.
        *args: Positional arguments to pass to `func`.
        **kwargs: Keyword arguments to pass to `func`.

    Returns:
        T: The result returned by `func`.
    """
    async with sessionmanager.session() as db:
        return await func(db, *args, **kwargs)
