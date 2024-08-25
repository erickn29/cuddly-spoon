from repositories.task import TaskRepository
from services.base import BaseService


class TaskService(BaseService):
    repository: TaskRepository = TaskRepository()
