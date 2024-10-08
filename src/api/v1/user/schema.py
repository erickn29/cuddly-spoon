from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserCreateInputSchema(BaseModel):
    email: str
    password: str


class UserCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    email: str


class UserUpdateDataSchema(BaseModel):
    email: str = None
    password: str = None
    is_active: bool = None


class UserUpdateInputSchema(BaseModel):
    user_id: UUID
    data: UserUpdateDataSchema


class UserUpdateOutputSchema(BaseModel):
    user_id: UUID
    email: str
    is_active: bool


class UserDeleteInputSchema(BaseModel):
    user_id: UUID


class UserDeleteOutputSchema(BaseModel):
    user_id: UUID


class UserRetrieveInputSchema(BaseModel):
    user_id: UUID


class UserRetrieveOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    email: str
    is_active: bool
