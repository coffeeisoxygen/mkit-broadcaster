from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class UserBaseConfig(BaseModel):
    """Base schema configuration for user-related schemas."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserCreate(UserBaseConfig):
    """Schema for creating single user."""

    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class UserOut(UserBaseConfig):
    """Schema for single user output."""

    id: int
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserinDB(UserOut):
    """Schema for user in database (includes hashed password)."""

    hashed_password: str


class UserUpdateProfile(UserBaseConfig):
    """Schema for updating user profile."""

    username: str | None = Field(None, min_length=3, max_length=50)
    full_name: str | None = Field(None, min_length=3, max_length=100)


class UserUpdatePassword(UserBaseConfig):
    """Schema for updating user password."""

    old_password: str = Field(..., min_length=6, max_length=100)
    new_password: str = Field(..., min_length=6, max_length=100)
    confirm_new_password: str = Field(..., min_length=6, max_length=100)

    @field_validator("confirm_new_password")
    @classmethod
    def passwords_match(cls, value: str, info: ValidationInfo) -> str:
        new_password = info.data.get("new_password")
        if new_password is not None and value != new_password:
            raise ValueError("New passwords do not match")
        return value


class UserLogin(UserBaseConfig):
    """Schema for user login."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class UserLoginResponse(UserOut):
    pass
