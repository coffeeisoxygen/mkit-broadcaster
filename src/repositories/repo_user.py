from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_user import User
from src.schemas.sch_user import UserCreate, UserUpdateProfile


# NOTE: Tambahkan fungsi update jika nanti ingin mendukung perubahan status/role user.
# NOTE: beberapa feature multi role masih ada, tetapi di-default-kan jadi superuser
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self) -> User | None:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_with_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_with_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=user_data.password,  # sudah di-hash di service
            is_active=True,  # Note: nanti diubah ketika fitur user management sudah ada
            is_superuser=True,  # Note: nanti diubah ketika fitur user management sudah ada
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_profile(self, user: User, profile: UserUpdateProfile) -> User:
        if profile.username is not None:
            user.username = profile.username
        if profile.full_name is not None:
            user.full_name = profile.full_name
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_password(self, user: User, new_password: str) -> User:
        user.hashed_password = new_password
        await self.db.commit()
        await self.db.refresh(user)
        return user
