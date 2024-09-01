from api.v1.bot_user.crud.schema import CommentInputSchema
from repositories.comment import CommentRepository
from services.base import BaseService


class CommentService(BaseService):
    repository: CommentRepository = CommentRepository()

    async def create(self, schema: CommentInputSchema):
        await self.repository.create(schema)
