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
    JoinChannelSchema,
    LeaveChannelSchema,
    TaskCreateSchema,
)
from core.exceptions import exception
from fastapi import APIRouter
from models.bot import Bot
from models.task import Task
from models.user import User
from services.bot import BotService
from services.task import TaskService
from services.user import UserService
from tasks.bot_tasks import joining_channel, leaving_channel, updating_bio
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
    bot_service = BotService()
    result = await bot_service.get(bot_id)
    return result


@router.post("/", status_code=201, response_model=BotCreateOutputSchema)
async def create(schema: BotCreateInputSchema):
    bot_service = BotService()
    result = await bot_service.create(schema)
    return result


@router.put("/", status_code=201, response_model=BotUpdateOutputSchema)
async def update(schema: BotUpdateInputSchema):
    bot_service = BotService()
    bot_object: Bot = await bot_service.get(schema.bot_id)
    if not bot_object:
        raise exception(404)
    if set(schema.data.config.bio.values()) != set(bot_object.config["bio"].values()):
        task_id = await bot_service.update_bot_bio(bot_object, schema)
        updating_bio.delay(bot_object.phone, schema.data.config.bio, task_id)
    if set(schema.data.config.channels) != set(bot_object.config["channels"]):
        channels = await bot_service.process_channels(
            schema.data.config.channels, bot_object.config["channels"]
        )
        if channels.get("leave"):
            task = TaskService()
            task_obj: Task = await task.create(
                TaskCreateSchema(
                    bot_id=bot_object.bot_id,
                    data=LeaveChannelSchema(channels=channels.get("leave")),
                )
            )
            leaving_channel.delay(bot_object.phone, channels["leave"], task_obj.task_id)
        if channels.get("join"):
            task = TaskService()
            task_obj: Task = await task.create(
                TaskCreateSchema(
                    bot_id=bot_object.bot_id,
                    data=JoinChannelSchema(channels=channels.get("join")),
                )
            )
            joining_channel.delay(bot_object.phone, channels["join"], task_obj.task_id)
    result = await bot_service.update(schema.bot_id, schema.data)
    return result


@router.delete("/", status_code=201, response_model=BotDeleteOutputSchema)
async def delete(schema: BotDeleteInputSchema):
    bot_service = BotService()
    result = await bot_service.delete(schema.bot_id)
    return BotDeleteInputSchema(bot_id=result)


@router.post("/list/", status_code=200, response_model=BotListOutputSchema)
async def item_list(schema: BotListInputSchema):
    user_service = UserService()
    user: User = await user_service.get(schema.user_id)
    return BotListOutputSchema(bots=user.bots)


@router.post("/comment/{phone}/", status_code=200)
async def test_comment(phone: str):
    bot = TelegramUserBot(phone)
    await bot.start_comments()
