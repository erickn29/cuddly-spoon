from pydantic import BaseModel


class UpdateBotBioInputSchema(BaseModel):
    phone: str
    first_name: str | None = None
    last_name: str | None = None
    about: str | None = None
