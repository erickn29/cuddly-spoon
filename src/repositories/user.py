from models.user import User
from repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
    id_column = f"{model.__tablename__.lower()}_id"
