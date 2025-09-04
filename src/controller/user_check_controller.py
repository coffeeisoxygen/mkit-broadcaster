from src.deps.deps_factory import get_user_services

from database.helper import run_in_session


async def user_exists():
    async def _logic(db):
        repo = get_user_services(db)["crud_service"].repo
        user = await repo.get_user()
        return user is not None

    return await run_in_session(_logic)


async def seed_user_if_empty(user_input):
    async def _logic(db):
        services = get_user_services(db)
        crud_service = services["crud_service"]
        db_user = await crud_service.repo.get_user()
        if not db_user:
            await crud_service.create_user(user_input)

    return await run_in_session(_logic)
