from repositories.comment import CommentRepository
from services.base import BaseService


class CommentService(BaseService):
    repository: CommentRepository = CommentRepository()
