import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi.testclient import TestClient
from core.models.models import Author, Book, Reader
from sqlalchemy.orm import Session


def test_create_author(client: TestClient, db: Session):
    """Тест создания автора."""
    response = client.post(
        "/authors/",
        json={
            "first_name": "Лев",
            "last_name": "Толстой",
            "date_of_birthday": "1828-09-09"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Лев"
    assert data["last_name"] == "Толстой"
    assert data["date_of_birthday"] == "1828-09-09"

    # Проверяем в базе данных
    author = db.query(Author).filter(Author.id == data["id"]).first()
    assert author is not None
    assert author.first_name == "Лев"


def test_get_author_by_id(client: TestClient, db: Session):
    """Тест получения автора по ID."""
    author = Author(first_name="Фёдор", last_name="Достоевский", date_of_birthday="1821-11-11")
    db.add(author)
    db.commit()
    db.refresh(author)

    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == author.id
    assert data["first_name"] == "Фёдор"
    assert data["last_name"] == "Достоевский"


def test_create_book(client: TestClient, db: Session):
    """Тест создания книги."""
    author = Author(first_name="Антон", last_name="Чехов", date_of_birthday="1860-01-29", is_deleted=0)
    db.add(author)
    db.commit()
    db.refresh(author)

    response = client.post(
        "/books/",
        json={
            "title": "Вишнёвый сад",
            "description": "A play",
            "balance_count": 5,
            "rest_count": 5,
            "author_ids": [author.id]
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Вишнёвый сад"
    assert len(data["authors"]) == 1
    assert data["authors"][0]["id"] == author.id


def test_borrow_and_return_book(client: TestClient, db: Session):
    """Тест создания записи о выдаче книги и её возврата."""
    # Создаем автора
    author = Author(first_name="Лев", last_name="Толстой", date_of_birthday="1828-09-09", is_deleted=0)
    db.add(author)
    db.commit()
    db.refresh(author)

    # Создаем читателя
    reader = Reader(first_name="Иван", last_name="Иванов", date_of_birthday="1990-01-01", email="ivanov@testmail.com", is_deleted=0)
    db.add(reader)
    db.commit()
    db.refresh(reader)

    # Создаем книгу
    book = Book(title="Война и мир", description="Роман-эпопея Льва Толстого.", balance_count=5, rest_count=5, is_deleted=0)
    book.authors.append(author)
    db.add(book)
    db.commit()
    db.refresh(book)

    # Проверяем начальное количество экземпляров
    assert book.rest_count == 5

    # Создаем выдачу
    borrow_response = client.post("/borrows/", json={"book_id": book.id, "reader_id": reader.id})
    assert borrow_response.status_code == 201

    # Проверяем уменьшение доступных экземпляров
    db.refresh(book)
    assert book.rest_count == 4

    # Возвращаем книгу
    return_response = client.patch(f"/borrows/{borrow_response.json()['id']}/return")
    assert return_response.status_code == 200

    # Проверяем увеличение доступных экземпляров
    db.refresh(book)
    assert book.rest_count == 5
