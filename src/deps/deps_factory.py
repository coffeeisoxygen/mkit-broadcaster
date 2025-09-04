from src.repositories.repo_user import UserRepository
from src.services.crud.user_auth_service import UserAuthService
from src.services.crud.user_crud_service import UserCrudService
from src.services.hasher.argon_hasher import ArgonPasswordHasher


def get_user_services(db):
    """Factory untuk semua user-related services."""
    repo = UserRepository(db)
    hasher = ArgonPasswordHasher()
    return {
        "auth_service": UserAuthService(repo, hasher),
        "crud_service": UserCrudService(repo, hasher),
    }


# nanti bisa tambah service lain di sini
# "telegram_service": TelegramService(config),
# "scheduler_service": AppSchedulerService(config),
