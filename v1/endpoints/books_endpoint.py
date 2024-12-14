from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.schemas.schemas import BookCreate, BookResponse
from core.models.models import Book, Author
from db import get_db
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Проверяем, существуют ли авторы с переданными ID
    authors = db.query(Author).filter(Author.id.in_(book.author_ids), Author.is_deleted == 0).all()
    if not authors or len(authors) != len(book.author_ids):
        raise HTTPException(
            status_code=400,
            detail="Некоторые авторы не найдены в базе данных или были удалены"
        )

    # Создаем новую книгу
    new_book = Book(
        title=book.title,
        description=book.description,
        balance_count=book.balance_count,
        rest_count=book.rest_count,
    )

    # Связываем книгу с авторами
    new_book.authors.extend(authors)

    # Сохраняем в базе данных
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.is_deleted == 0).all()
    return books


@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id, Book.is_deleted == 0).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга с указанным ID не найдена или был удалена ранее")
    return book


@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    # Ищем книгу по ID
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга с указанным ID не найдена")

    # Обновляем данные книги
    book.title = updated_book.title
    book.description = updated_book.description
    book.balance_count = updated_book.balance_count
    book.rest_count = updated_book.rest_count
    book.updated_at = datetime.utcnow()

    # Если в запросе указаны авторы, обновляем связь
    if updated_book.author_ids:
        # Проверяем существование указанных авторов
        authors = db.query(Author).filter(Author.id.in_(updated_book.author_ids), Author.is_deleted == 0).all()
        if not authors or len(authors) != len(updated_book.author_ids):
            raise HTTPException(
                status_code=400,
                detail="Некоторые авторы не найдены в базе данных"
            )
        # Обновляем связь с авторами
        book.authors = authors

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{id}", status_code=204)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id, Book.is_deleted == 0).first()
    if not book:
        raise HTTPException(status_code=404, detail="Автор с указанным ID не найден или был удален ранее")
    book.is_deleted = 1
    book.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(book)
    return {"message": f"Книга - {id} успешно удалена"}
