from src.deps.deps_factory import get_user_services

from database.helper import run_in_session


async def login(user_input):
    """Proses login user."""

    async def _logic(db):
        services = get_user_services(db)
        auth_service = services["auth_service"]
        return await auth_service.login(user_input)

    return await run_in_session(_logic)
