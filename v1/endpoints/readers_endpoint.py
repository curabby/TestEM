from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.schemas.schemas import ReaderCreate, ReaderResponse
from core.models.models import Reader
from db import get_db
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=ReaderResponse, status_code=201)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    new_reader = Reader(
        first_name=reader.first_name,
        last_name=reader.last_name,
        date_of_birthday=reader.date_of_birthday,
        email=reader.email
    )
    try:
        db.add(new_reader)
        db.commit()
        db.refresh(new_reader)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email должен быть уникальным")
    return new_reader


@router.get("/", response_model=List[ReaderResponse])
def get_readers(db: Session = Depends(get_db)):
    readers = db.query(Reader).filter(Reader.is_deleted == 0).all()
    return readers


@router.get("/{id}", response_model=ReaderResponse)
def get_reader(id: int, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.id == id, Reader.is_deleted == 0).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель с указанным ID не найден или был удален ранее")
    return reader


@router.put("/{id}", response_model=ReaderResponse)
def update_reader(id: int, updated_reader: ReaderCreate, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.id == id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель с указанным ID не найден")
    reader.first_name = updated_reader.first_name
    reader.last_name = updated_reader.last_name
    reader.date_of_birthday = updated_reader.date_of_birthday
    reader.email = updated_reader.email
    reader.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{id}", status_code=204)
def delete_reader(id: int, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.id == id, Reader.is_deleted == 0).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель с указанным ID не найден или был удален ранее")
    reader.is_deleted = 1
    reader.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(reader)
    return {"message": f"Читатель - {id} удален успешно"}