from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.schemas.schemas import BorrowCreate, BorrowResponse
from core.models.models import Borrow, Book, Reader
from db import get_db
from typing import List
from datetime import date

router = APIRouter()



@router.post("/", response_model=BorrowResponse, status_code=201)
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
    # Проверять наличие доступных экземпляров книги при создании записи о выдаче
    book = db.query(Book).filter(Book.id == borrow.book_id, Book.is_deleted == 0).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга с указанным ID не найдена")
    if book.rest_count == 0:
        raise HTTPException(status_code=400, detail="Нет доступных экземпляров книги")

    # Проверяем, существует ли читатель
    reader = db.query(Reader).filter(Reader.id == borrow.reader_id, Reader.is_deleted == 0).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель с указанным ID не найден")

    # Создаем запись о выдаче
    new_borrow = Borrow(
        book_id=borrow.book_id,
        reader_id=borrow.reader_id,
        issue_date=date.today(),
    )
    # Уменьшаем количество доступных экземпляров книги
    book.rest_count -= 1

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow



@router.get("/", response_model=List[BorrowResponse])
def get_borrows(db: Session = Depends(get_db)):
    borrows = db.query(Borrow).all()
    return borrows



@router.get("/{id}", response_model=BorrowResponse)
def get_borrow(id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Запись о выдаче с указанным ID не найдена")
    return borrow


# Возврат
@router.patch("/{id}/return", response_model=BorrowResponse)
def return_borrow(id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Запись о выдаче с указанным ID не найдена")
    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Книга уже возвращена")

    # Устанавливаем дату возврата
    borrow.return_date = date.today()

    # Увеличиваем количество доступных экземпляров книги
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.rest_count += 1
    db.commit()
    db.refresh(borrow)
    return borrow

