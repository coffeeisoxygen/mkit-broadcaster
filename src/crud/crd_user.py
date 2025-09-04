"""crud untuk user."""

import hashlib
from collections.abc import Sequence

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_user import User
from src.schemas.sch_user import (
    AdminCreateUser,
    AdminUpdateUser,
    UserCreate,
    UserOut,
    UserUpdatePassword,
    UserUpdateProfile,
)

from custom.exception import (
    UserCreationError,
    UserDuplicateError,
    UserGenericError,
    UserNotFoundError,
    UserPasswordError,
)


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Mengambil user berdasarkan username."""
    try:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            logger.bind(username=username).warning("User not found by username")
            raise UserNotFoundError(f"User '{username}' not found.")
    except UserNotFoundError:
        raise
    except Exception as exc:
        logger.bind(username=username, error=str(exc)).error(
            "Error get_user_by_username"
        )
        raise UserGenericError(f"Failed to get user by username: {username}") from exc
    else:
        return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Mengambil user berdasarkan ID."""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            logger.bind(user_id=user_id).warning("User not found by id")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
    except UserNotFoundError:
        raise
    except Exception as exc:
        logger.bind(user_id=user_id, error=str(exc)).error("Error get_user_by_id")
        raise UserGenericError(f"Failed to get user by id: {user_id}") from exc
    else:
        return user


async def get_all_users(db: AsyncSession) -> Sequence[User]:
    """Mengambil semua user."""
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except Exception as exc:
        logger.bind(error=str(exc)).error("Error get_all_users")
        raise UserGenericError("Failed to get all users") from exc


async def admin_create_user(db: AsyncSession, user: AdminCreateUser) -> User:
    """Membuat user baru oleh admin."""
    try:
        try:
            existing = await get_user_by_username(db, user.username)
            if existing:
                logger.bind(username=user.username).warning(
                    "Duplicate user creation attempt"
                )
                raise UserDuplicateError(f"User '{user.username}' already exists.")
        except UserNotFoundError:
            pass

        new_user = User(
            username=user.username,
            full_name=user.full_name,
            hashed_password=hash_password(user.password),
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.bind(username=user.username).info("Admin created user")
    except UserDuplicateError:
        raise
    except Exception as exc:
        logger.bind(username=user.username, error=str(exc)).error(
            "Error admin_create_user"
        )
        raise UserCreationError(f"Failed to create user '{user.username}'") from exc
    else:
        return new_user


async def admin_update_user(
    db: AsyncSession, user_id: int, user_update: AdminUpdateUser
) -> User | None:
    """Memperbarui detail user oleh admin."""
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            logger.bind(user_id=user_id).warning("User not found for update")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        user.full_name = user_update.full_name
        user.is_active = user_update.is_active
        user.is_superuser = user_update.is_superuser
        await db.commit()
        await db.refresh(user)
        logger.bind(user_id=user_id).info("Admin updated user")
    except UserNotFoundError:
        raise
    except Exception as exc:
        logger.bind(user_id=user_id, error=str(exc)).error("Error admin_update_user")
        raise UserGenericError(f"Failed to update user id: {user_id}") from exc
    else:
        return user


def hash_password(password: str) -> str:
    """Hash password sederhana, bisa diganti dengan algoritma lain."""
    return hashlib.sha256(password.encode()).hexdigest()


async def create_user(db: AsyncSession, user: UserCreate) -> UserOut:
    """Membuat user baru (bukan admin)."""
    try:
        try:
            existing = await get_user_by_username(db, user.username)
            if existing:
                logger.bind(username=user.username).warning(
                    "Duplicate user creation attempt"
                )
                raise UserDuplicateError(f"User '{user.username}' already exists.")
        except UserNotFoundError:
            pass

        new_user = User(
            username=user.username,
            full_name=user.full_name,
            hashed_password=hash_password(user.password),
            is_active=True,
            is_superuser=False,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.bind(username=user.username).info("User created")
    except UserDuplicateError:
        raise
    except Exception as exc:
        logger.bind(username=user.username, error=str(exc)).error("Error create_user")
        raise UserCreationError(f"Failed to create user '{user.username}'") from exc
    else:
        return UserOut.model_validate(new_user)


async def update_user_profile(
    db: AsyncSession, user_id: int, profile: UserUpdateProfile
) -> UserOut | None:
    """User update profile sendiri."""
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            logger.bind(user_id=user_id).warning("User not found for profile update")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        user.full_name = profile.full_name
        await db.commit()
        await db.refresh(user)
        logger.bind(user_id=user_id).info("User updated profile")
    except UserNotFoundError:
        raise
    except Exception as exc:
        logger.bind(user_id=user_id, error=str(exc)).error("Error update_user_profile")
        raise UserGenericError(
            f"Failed to update profile for user id: {user_id}"
        ) from exc
    else:
        return UserOut.model_validate(user)


async def update_user_password(
    db: AsyncSession, user_id: int, password_data: UserUpdatePassword
) -> bool:
    """User ganti password sendiri."""
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            logger.bind(user_id=user_id).warning("User not found for password update")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        if user.hashed_password != hash_password(password_data.old_password):
            logger.bind(user_id=user_id).warning("Old password mismatch")
            raise UserPasswordError("Old password does not match.")
        user.hashed_password = hash_password(password_data.new_password)
        await db.commit()
        await db.refresh(user)
        logger.bind(user_id=user_id).info("User updated password")
    except UserNotFoundError:
        raise
    except UserPasswordError:
        raise
    except Exception as exc:
        logger.bind(user_id=user_id, error=str(exc)).error("Error update_user_password")
        raise UserPasswordError(
            f"Failed to update password for user id: {user_id}"
        ) from exc
    else:
        return True


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Menghapus user berdasarkan ID."""
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            logger.bind(user_id=user_id).warning("User not found for delete")
            raise UserNotFoundError(f"User id '{user_id}' not found.")
        await db.delete(user)
        await db.commit()
        logger.bind(user_id=user_id).info("User deleted")
    except UserNotFoundError:
        raise
    except Exception as exc:
        logger.bind(user_id=user_id, error=str(exc)).error("Error delete_user")
        raise UserGenericError(f"Failed to delete user id: {user_id}") from exc
    else:
        return True
