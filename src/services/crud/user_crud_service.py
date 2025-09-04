from loguru import logger
from src.custom.exception import (
    UserCreationError,
    UserDuplicateError,
    UserNotFoundError,
)
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import UserCreate, UserinDB, UserOut, UserUpdateProfile

from services.hasher.intf_hasher import IPasswordHasher


class UserCrudService:
    def __init__(self, repo: UserRepository, hasher: IPasswordHasher):
        self.repo: UserRepository = repo
        self.hasher: IPasswordHasher = hasher

    async def get_profile(self, user_id: int) -> UserOut:
        user = await self.repo.get_user_with_id(user_id)
        if not user:
            logger.bind(user_id=user_id).warning("No user found with id.")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        return UserOut.model_validate(user)

    async def get_profile_with_password(self, user_id: int) -> UserinDB:
        """Hanya untuk internal (misal update password)."""
        user = await self.repo.get_user_with_id(user_id)
        if not user:
            logger.bind(user_id=user_id).warning("No user found with id.")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        return UserinDB.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserOut:
        """Cek duplicate username dulu → create user baru pakai hashed password."""
        with logger.contextualize(username=user_data.username):
            existing = await self.repo.get_user_with_username(user_data.username)
            if existing:
                logger.warning("Duplicate user creation.")
                raise UserDuplicateError(f"User '{user_data.username}' already exists.")

            # hashing di service layer
            user_data.password = self.hasher.hash(user_data.password)

            user = await self.repo.create_user(user_data)
            if not user:
                logger.error("Failed to create user.")
                raise UserCreationError(f"Failed to create user '{user_data.username}'")

            logger.info("Created user.")
            return UserOut.model_validate(user)

    async def update_profile(self, user_id: int, profile: UserUpdateProfile) -> UserOut:
        """Update pakai user_id (username bisa berubah, jadi jangan rely ke username)."""
        user = await self.repo.get_user_with_id(user_id)
        if not user:
            logger.bind(user_id=user_id).error("No user found for update.")
            raise UserNotFoundError(f"User id '{user_id}' not found.")

        with logger.contextualize(username=profile.username or user.username):
            # kalau username mau diganti, harus dicek duplicate
            if profile.username and profile.username != user.username:
                existing = await self.repo.get_user_with_username(profile.username)
                if existing:
                    logger.warning("Duplicate username update.")
                    raise UserDuplicateError(
                        f"Username '{profile.username}' already exists."
                    )

            updated = await self.repo.update_profile(user, profile)
            logger.info("Profile updated.")
            return UserOut.model_validate(updated)

    async def update_password(self, user_id: int, new_password: str) -> UserOut:
        """Selalu pakai user_id supaya stabil (username bisa berubah)."""
        user = await self.repo.get_user_with_id(user_id)
        if not user:
            logger.bind(user_id=user_id).error("No user found for password update.")
            raise UserNotFoundError(f"User id '{user_id}' not found.")

        hashed_password = self.hasher.hash(new_password)
        updated = await self.repo.update_password(user, hashed_password)

        logger.bind(username=user.username).info("Password updated.")
        return UserOut.model_validate(updated)
