from datetime import date
from sqlalchemy import String, Text, ForeignKey, CheckConstraint,func, Table, Column, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass


# Промежуточная таблица для связи "многие ко многим"
book_author_association = Table(
    "book_author",
    Base.metadata,
    Column("author_id", ForeignKey("author.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    date_of_birthday: Mapped[date] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[date | None] = mapped_column(nullable=True)
    is_deleted: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    deleted_at: Mapped[date | None] = mapped_column(nullable=True)
    # Связь с книгами
    books: Mapped[List["Book"]] = relationship(
        secondary=book_author_association, back_populates="authors"
    )


class Reader(Base):
    __tablename__ = "readers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    date_of_birthday: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    created_at: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[date | None] = mapped_column(nullable=True)
    is_deleted: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    deleted_at: Mapped[date | None] = mapped_column(nullable=True)
    # Связь с записями о выдаче книг
    borrows: Mapped[List["Borrow"]] = relationship(back_populates="reader")




class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    balance_count: Mapped[int | None] = mapped_column(nullable=True)  # Всего книг на балансе
    rest_count: Mapped[int | None] = mapped_column(nullable=True)  # Всего книг в наличии
    created_at: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[date | None] = mapped_column(nullable=True)
    is_deleted: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    deleted_at: Mapped[date | None] = mapped_column(nullable=True)

    # Связь с автором
    authors: Mapped[List[Author]] = relationship(
        secondary=book_author_association, back_populates="books"
    )

    # Связь с записями о взятии книги
    borrows: Mapped[List["Borrow"]] = relationship(back_populates="book")

    # Ограничения на уровне таблицы
    __table_args__ = (
        CheckConstraint('balance_count >= 0', name='check_balance_count_non_negative'),
        CheckConstraint('rest_count >= 0', name='check_rest_count_non_negative'),
    )


class Borrow(Base):
    __tablename__ = "borrows"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"), nullable=False)  # Внешний ключ к читателю
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))  # Внешний ключ к книгам
    issue_date: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)  # Дата выдачи книги/книг
    return_date: Mapped[date | None] = mapped_column(nullable=True) # Дата возврата книги (может быть NULL)
    # Связь с пользователем, взявшим книги (один ко многим)
    reader: Mapped["Reader"] = relationship(back_populates="borrows")

    # Связь с книгой
    book: Mapped["Book"] = relationship(back_populates="borrows")