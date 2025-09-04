from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_user import User
from src.schemas.sch_user import UserCreate, UserUpdatePassword, UserUpdateProfile


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------- GETTERS ----------------
    async def get_user_with_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_users(self) -> list[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_users_by_active(self, active: bool = True) -> list[User]:
        stmt = select(User).where(User.is_active == active)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------- CREATE ----------------
    async def create_user(self, user_data: UserCreate) -> User:
        """Input schema, output SQLAlchemy entity.
        NOTE: password must already be hashed before calling repo.
        """
        user = User(
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=user_data.password,  # sudah di-hash di service
            is_active=True,
            is_superuser=False,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    # ---------------- UPDATE ----------------
    async def update_user_profile(self, user: User, profile: UserUpdateProfile) -> User:
        user.full_name = profile.full_name
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update_user_password(
        self, user: User, password_data: UserUpdatePassword
    ) -> User:
        """NOTE: password must already be hashed before calling repo."""
        user.hashed_password = password_data.new_password
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        """Generic update when object already mutated before."""
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def set_active(self, user_id: int, active: bool = True) -> User | None:
        user = await self.get_user_with_id(user_id)
        if not user:
            return None
        user.is_active = active
        await self.db.flush()
        await self.db.refresh(user)
        return user

    # ---------------- DELETE ----------------
    async def delete_user(self, user: User) -> bool:
        await self.db.delete(user)
        await self.db.flush()
        return True

    async def delete_user_by_id(self, user_id: int) -> bool:
        user = await self.get_user_with_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.flush()
        return True
