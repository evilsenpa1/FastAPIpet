from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import ForeignKey, Table, Column


# class BookAuthor(Base):
#     __tablename__ = "book_authors"

#     book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
#     author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    authors: Mapped[List["AuthorModel"]] = relationship(secondary=association_table, back_populates="books", lazy="selectin")
    description: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    day: Mapped[int] = mapped_column()


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column()
    books: Mapped[List["BookModel"]] = relationship(secondary=association_table, back_populates="authors", lazy="selectin")
