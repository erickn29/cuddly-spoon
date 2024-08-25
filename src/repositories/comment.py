from models.comment import Comment
from repositories.base import SQLAlchemyRepository


class CommentRepository(SQLAlchemyRepository):
    model = Comment
    id_column = f"{model.__tablename__.lower()}_id"
