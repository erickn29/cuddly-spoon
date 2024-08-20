from pydantic import BaseModel


class TestSchema(BaseModel):
    phone: str
