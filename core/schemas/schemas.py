from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import date

"""Таблица авторов"""


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birthday: date  # YYYY-MM-DD


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    date_of_birthday: date
    created_at: date
    updated_at: Optional[date]
    is_deleted: int
    deleted_at: Optional[date]



"""Таблица читателей"""


class ReaderCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birthday: date  # YYYY-MM-DD
    email: EmailStr


class ReaderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    date_of_birthday: date
    email: str
    created_at: date
    updated_at: Optional[date]
    is_deleted: int
    deleted_at: Optional[date]


"""Таблица книги"""


class BookCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str]
    balance_count: Optional[int]
    rest_count: Optional[int]
    author_ids: List[int]  # Список ID авторов для привязки к книге


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    balance_count: Optional[int]
    rest_count: Optional[int]
    authors: List[AuthorResponse]
    updated_at: Optional[date]
    is_deleted: int
    deleted_at: Optional[date]



"""Таблица запись о выдаче книг"""

class BorrowCreate(BaseModel):
    book_id: int
    reader_id: int


class BorrowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    reader_id: int
    issue_date: date
    return_date: Optional[date]
