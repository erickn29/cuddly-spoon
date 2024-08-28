from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BotConfig(BaseModel):
    prompt: list[str]
    comment_text: list[str]


class BotCreateInputSchema(BaseModel):
    user_id: UUID
    phone: str
    alias: str = None
    config: BotConfig


class BotCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bot_id: UUID
    user_id: UUID
    phone: str
    alias: str | None = None
    config: BotConfig


class BotUpdateDataSchema(BaseModel):
    alias: str = None
    config: BotConfig
    is_stopped: bool = False
    is_active: bool = False


class BotUpdateInputSchema(BaseModel):
    bot_id: UUID
    data: BotUpdateDataSchema


class BotUpdateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bot_id: UUID
    user_id: UUID
    phone: str
    alias: str | None = None
    config: BotConfig
    is_stopped: bool
    is_active: bool


class BotDeleteInputSchema(BaseModel):
    bot_id: UUID


class BotDeleteOutputSchema(BaseModel):
    bot_id: UUID


class BotRetrieveInputSchema(BaseModel):
    bot_id: UUID


class BotRetrieveOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bot_id: UUID
    user_id: UUID
    phone: str
    alias: str | None = None
    config: BotConfig
    is_stopped: bool
    is_active: bool
    created_at: datetime


class BotListInputSchema(BaseModel):
    user_id: UUID


class BotListOutputSchema(BaseModel):
    bots: list[BotRetrieveOutputSchema]


class BotAuthPhoneInputSchema(BaseModel):
    phone: str


class BotAuthPhoneCodeInputSchema(BaseModel):
    phone: str
    code: str


class BotAuthResultOutputSchema(BaseModel):
    status: bool


class BotJoinChannelInputSchema(BaseModel):
    bot_id: UUID
    channels: list[str]


class BotLeaveChannelInputSchema(BaseModel):
    bot_id: UUID
    channels: list[str]


class JoinChannelSchema(BaseModel):
    type: str = "join-channels"
    channels: list[str]


class LeaveChannelSchema(BaseModel):
    type: str = "leave-channels"
    channels: list[str]


class TaskCreateSchema(BaseModel):
    bot_id: UUID
    is_executed: bool = False
    data: JoinChannelSchema | LeaveChannelSchema


class TaskUpdateSchema(BaseModel):
    is_executed: bool = False
