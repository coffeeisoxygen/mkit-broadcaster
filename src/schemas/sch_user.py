"""schemas for user generation by admin."""

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class UserBase(BaseModel):
    """Base model for user."""

    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Model for creating a user."""

    password: str = Field(..., min_length=6, max_length=100)


class AdminCreateUser(UserCreate):
    """Model for creating a user."""

    is_superuser: bool
    is_active: bool
    admin_password: str = Field(..., min_length=6, max_length=100)


class UserOut(UserBase):
    """Model for outputting user data."""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: str
    updated_at: str


class UserInDB(UserOut):
    """Model for user in database with hashed password."""

    hashed_password: str


class UserUpdatePassword(BaseModel):
    """Model for updating user password."""

    model_config = ConfigDict(from_attributes=True)

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


class AdminUpdateUser(BaseModel):
    """Model for admin updating user details."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=3, max_length=100)
    is_active: bool
    is_superuser: bool
    admin_password: str = Field(..., min_length=6, max_length=100)


class UserUpdateProfile(BaseModel):
    """Model for user updating their profile."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=3, max_length=100)
