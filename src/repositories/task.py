from models.task import Task
from repositories.base import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
    id_column = f"{model.__tablename__.lower()}_id"
