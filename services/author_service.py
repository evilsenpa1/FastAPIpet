from models.book import BookModel
from repository.author import AuthorRepository


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo
