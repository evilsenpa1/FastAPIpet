from datetime import date

from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import ForeignKey, Table, Column


association_table = Table(
    "association_table",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    authors: Mapped[List["AuthorModel"]] = relationship(secondary=association_table, back_populates="books", lazy="selectin")
    description: Mapped[str] = mapped_column()
    pub_date: Mapped[date] = mapped_column()
    file_path: Mapped[str] = mapped_column(nullable=True)


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column()
    books: Mapped[List["BookModel"]] = relationship(secondary=association_table, back_populates="authors", lazy="selectin")
