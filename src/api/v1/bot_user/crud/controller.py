from api.v1.bot_user.crud.schema import (
    BotAuthPhoneCodeInputSchema,
    BotAuthPhoneInputSchema,
    BotAuthResultOutputSchema,
    BotCreateInputSchema,
    BotCreateOutputSchema,
    BotDeleteInputSchema,
    BotDeleteOutputSchema,
    BotListInputSchema,
    BotListOutputSchema,
    BotRetrieveOutputSchema,
    BotUpdateInputSchema,
    BotUpdateOutputSchema,
)
from fastapi import APIRouter
from models.user import User
from services.bot import BotService
from services.user import UserService
from utils.telegram.user_bot.bot import TelegramUserBot


router = APIRouter()


@router.post("/auth/check/", response_model=BotAuthResultOutputSchema)
async def check_auth(schema: BotAuthPhoneInputSchema):
    bot = TelegramUserBot(schema.phone)
    user_is_authorized = await bot.check_is_authorized()
    return BotAuthResultOutputSchema(status=user_is_authorized)


@router.post("/auth/request-code/", response_model=BotAuthResultOutputSchema)
async def request_code(schema: BotAuthPhoneInputSchema):
    bot = TelegramUserBot(schema.phone)
    code_is_sent_to_user = await bot.request_verification_code()
    return BotAuthResultOutputSchema(status=code_is_sent_to_user)


@router.post("/auth/send-code/", response_model=BotAuthResultOutputSchema)
async def sign_in(schema: BotAuthPhoneCodeInputSchema):
    bot = TelegramUserBot(schema.phone)
    auth_is_success = await bot.sign_in_with_code(schema.code)
    return BotAuthResultOutputSchema(status=auth_is_success)


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
