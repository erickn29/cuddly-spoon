from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BotConfigInputSchema(BaseModel):
    prompt: list[str] = []
    comment_text: list[str] = []
    channels: list[str] = []
    bio: dict[str, str] = {
        "first_name": "",
        "last_name": "",
        "about": "",
    }


class BotConfigOutputSchema(BaseModel):
    prompt: list[str]
    comment_text: list[str]
    channels: list[str]
    bio: dict[str, str]


class BotCreateInputSchema(BaseModel):
    user_id: UUID
    phone: str
    alias: str = None
    config: BotConfigInputSchema


class BotCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bot_id: UUID
    user_id: UUID
    phone: str
    alias: str | None = None
    config: BotConfigOutputSchema


class BotUpdateDataSchema(BaseModel):
    alias: str | None = None
    config: BotConfigInputSchema | None = None
    is_stopped: bool | None = None
    is_active: bool | None = None


class BotUpdateInputSchema(BaseModel):
    bot_id: UUID
    data: BotUpdateDataSchema


class BotUpdateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bot_id: UUID
    user_id: UUID
    phone: str
    alias: str | None = None
    config: BotConfigOutputSchema
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
    config: BotConfigOutputSchema
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


class UpdateBioSchema(BaseModel):
    type: str = "update-bio"
    bio: dict[str, Any] = {}


class BotUpdateBioInputSchema(BaseModel):
    bot_id: UUID
    first_name: str = Field(max_length=70)
    last_name: str = Field(max_length=64)
    about: str = Field(max_length=70)


class TaskCreateSchema(BaseModel):
    bot_id: UUID
    is_executed: bool = False
    data: JoinChannelSchema | LeaveChannelSchema | UpdateBioSchema


class TaskUpdateSchema(BaseModel):
    is_executed: bool = False
