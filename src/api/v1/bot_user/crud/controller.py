from api.v1.bot_user.crud.schema import (
    BotCreateInputSchema,
    BotCreateOutputSchema,
    BotDeleteInputSchema,
    BotDeleteOutputSchema,
    BotRetrieveOutputSchema,
    BotUpdateInputSchema,
    BotUpdateOutputSchema, BotRetrieveInputSchema, BotListOutputSchema,
    BotListInputSchema,
)
from fastapi import APIRouter

from models.user import User
from services.bot import BotService
from services.user import UserService

router = APIRouter()


@router.get("/{bot_id}/", status_code=200, response_model=BotRetrieveOutputSchema)
async def retrieve(bot_id: str):
    user_service = BotService()
    result = await user_service.get(bot_id)
    return result


@router.post("/", status_code=201, response_model=BotCreateOutputSchema)
async def create(schema: BotCreateInputSchema):
    user_service = BotService()
    result = await user_service.create(schema)
    return result


@router.put("/", status_code=201, response_model=BotUpdateOutputSchema)
async def update(schema: BotUpdateInputSchema):
    user_service = BotService()
    result = await user_service.update(schema.bot_id, schema.data)
    return result


@router.delete("/", status_code=201, response_model=BotDeleteOutputSchema)
async def delete(schema: BotDeleteInputSchema):
    user_service = BotService()
    result = await user_service.delete(schema.bot_id)
    return BotDeleteInputSchema(bot_id=result)


@router.post("/list/", status_code=200, response_model=BotListOutputSchema)
async def item_list(schema: BotListInputSchema):
    user_service = UserService()
    user: User = await user_service.get(schema.user_id)
    return BotListOutputSchema(bots=user.bots)

