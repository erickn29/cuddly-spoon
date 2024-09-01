from api.v1.bot_user.crud.schema import TaskCreateSchema
from models.task import Task
from repositories.task import TaskRepository
from services.base import BaseService


class TaskService(BaseService):
    repository: TaskRepository = TaskRepository()

    async def create(self, schema: TaskCreateSchema) -> Task:
        return await self.repository.create(schema)
