from schemas.book import BookAddSchema, AuthorAddSchema, BookDeleteSchema, BookUpdateSchema, AuthorUpdateSchema, AuthorDeleteSchema
from db.session import SessionDep
from models.book import BookModel, AuthorModel
from sqlalchemy import select
from fastapi import HTTPException




async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()


async def get_authors(session: SessionDep):
    query = select(AuthorModel)
    result = await session.execute(query)
    return result.scalars().all()


async def add_book(data: BookAddSchema, session: SessionDep):
    author_objects = []
    for author_name in data.authors:
        result = await session.execute(select(AuthorModel).filter(AuthorModel.author == author_name))

        author = result.scalars().first()

        if not author:
            author = AuthorModel(author=author_name)
            session.add(author)

        author_objects.append(author)

    new_book= BookModel(
        name = data.name,
        authors = author_objects,
        description = data.description,
        year = data.year,
        month = data.month,
        day = data.day,
    )
    session.add(new_book)
    await session.commit()
    return {"status": "success"}


async def update_book(data: BookUpdateSchema, session: SessionDep):

    result = await session.execute(select(BookModel).filter(BookModel.id == data.id))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.name = "New name"
    book.year = 6666
    
    await session.commit()
    return {"status": "success"}


async def delete_book(data: BookDeleteSchema, session: SessionDep):

    result = await session.execute(select(BookModel).filter(BookModel.id == data.id))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"status": "success"}



async def add_author(data: AuthorAddSchema, session: SessionDep):

    new_author= AuthorModel(
        author = data.author,
    )
    session.add(new_author)
    await session.commit()
    return {"status": "success"}


async def update_author(data: AuthorUpdateSchema, session: SessionDep):

    result = await session.execute(select(AuthorModel).filter(AuthorModel.id == data.id))
    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    author.name = "New author"
    
    await session.commit()
    return {"status": "success"}


async def delete_author(data: AuthorDeleteSchema, session: SessionDep):

    result = await session.execute(select(AuthorModel).filter(AuthorModel.id == data.id))
    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(author)
    await session.commit()
    return {"status": "success"}