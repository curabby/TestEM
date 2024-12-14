from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.schemas.schemas import AuthorCreate, AuthorResponse
from core.models.models import Author
from db import get_db
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=AuthorResponse, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(
        first_name=author.first_name,
        last_name=author.last_name,
        date_of_birthday=author.date_of_birthday,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=List[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).filter(Author.is_deleted == 0).all()
    return authors


@router.get("/{id}", response_model=AuthorResponse)
def get_author(id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == id, Author.is_deleted == 0).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор с указанным ID не найден или был удален ранее")
    return author


@router.put("/{id}", response_model=AuthorResponse)
def update_author(id: int, updated_author: AuthorCreate, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор с указанным ID не найден")
    author.first_name = updated_author.first_name
    author.last_name = updated_author.last_name
    author.date_of_birthday = updated_author.date_of_birthday
    author.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(author)
    return author


@router.delete("/{id}", status_code=204)
def delete_author(id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == id, Author.is_deleted == 0).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор с указанным ID не найден или был удален ранее")

    author.is_deleted = 1
    author.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(author)
    return {"message": f"Автор - {id} успешно удален"}
