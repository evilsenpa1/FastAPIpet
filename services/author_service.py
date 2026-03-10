from models.book_model import BookModel
from repository.author_repo import AuthorRepository


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo
