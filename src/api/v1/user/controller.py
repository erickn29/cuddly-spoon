from api.v1.user.schema import (
    UserCreateInputSchema,
    UserCreateOutputSchema,
    UserDeleteInputSchema,
    UserDeleteOutputSchema,
    UserRetrieveOutputSchema,
    UserUpdateInputSchema,
    UserUpdateOutputSchema,
)
from fastapi import APIRouter
from services.user import UserService


router = APIRouter()


@router.get("/{user_id}/", status_code=200, response_model=UserRetrieveOutputSchema)
async def retrieve(user_id: str):
    user_service = UserService()
    result = await user_service.get(user_id)
    return result


@router.post("/", status_code=201, response_model=UserCreateOutputSchema)
async def create(schema: UserCreateInputSchema):
    user_service = UserService()
    result = await user_service.create(schema)
    return result


@router.put("/", status_code=201, response_model=UserUpdateOutputSchema)
async def update(schema: UserUpdateInputSchema):
    user_service = UserService()
    result = await user_service.update(schema.user_id, schema.data)
    return result


@router.delete("/", status_code=201, response_model=UserDeleteOutputSchema)
async def delete(schema: UserDeleteInputSchema):
    user_service = UserService()
    result = await user_service.delete(schema.user_id)
    return UserDeleteInputSchema(user_id=result)
