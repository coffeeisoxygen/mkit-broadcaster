from loguru import logger
from src.custom.exception import UserNotFoundError, UserPasswordError
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import UserLogin, UserLoginResponse

from services.hasher.argon_hasher import IPasswordHasher


class UserAuthService:
    def __init__(self, repo: UserRepository, hasher: IPasswordHasher) -> None:
        self.repo = repo
        self.hasher = hasher

    async def login(self, user: UserLogin) -> UserLoginResponse | None:
        """Check username and password, return user info if valid."""
        db_user = await self.repo.get_user_with_username(user.username)
        if not db_user:
            logger.bind(username=user.username).warning("Login failed: user not found.")
            raise UserNotFoundError(f"User '{user.username}' not found.")
        if not self.hasher.verify(db_user.hashed_password, user.password):
            logger.bind(username=user.username).warning("Login failed: wrong password.")
            raise UserPasswordError("Incorrect password.")
        logger.bind(username=user.username).info("Login success.")
        return UserLoginResponse.model_validate(db_user)
