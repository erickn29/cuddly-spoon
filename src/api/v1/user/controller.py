from fastapi import APIRouter

from api.v1.user.schema import UserCreateOutputSchema, UserCreateInputSchema
from services.user import UserService

router = APIRouter()


@router.post("/", status_code=201, response_model=UserCreateOutputSchema)
async def create(schema: UserCreateInputSchema):
    user_service = UserService()
    result = await user_service.create(schema)
    return result
