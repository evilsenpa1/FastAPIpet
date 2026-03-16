from models.book_model import AuthorModel
from repository.author_repo import AuthorRepository
from schemas.author_schema import AuthorAddSchema, AuthorPatchSchema
from fastapi import HTTPException
from utils import file_manager
from repository.book_repo import BookRepository


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def get_all_authors(self):
        return await self.repo.get_all()
    
    async def get_author_by_id(self, id: int):
        return await self.repo.get_by_id(id)

    async def create_author(self, data: AuthorAddSchema) -> AuthorModel:
        return await self.repo.create(data)
    
    async def patch_author(self, id: int, data: AuthorPatchSchema) -> AuthorModel:
        return await self.repo.patch(id, data)
    
    async def delete_author(self, id: int, book_repo: BookRepository):
        author = await self.repo.get_by_id(id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        
        orphaned_books = [
            book for book in author.books
            if len(book.authors) == 1
        ]

        for book in orphaned_books:
            if book.file_path:
                file_manager.delete_file(book.file_path)
            await book_repo.delete(book.id)

    
        return await self.repo.delete(id)

