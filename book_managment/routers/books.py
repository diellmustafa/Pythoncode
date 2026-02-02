import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from book_managment.models.book import BookCreate, Book
from book_managment.database import get_db_connection
from book_managment.auth.security import get_api_key

router = APIRouter()

@router.get("/", response_model=List[Book])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author_id FROM books")
    books = cursor.fetchall()
    conn.close()
    return [{
        "id": book[0],
        "title": book[1],
        "author_id": book[2],
        "book_link": book[3],
        "genres": book[4].split(",") if book[4] else[],
        "average_rating": book[5],
        "published_year": book[6]
    }
        for book in books
    ]

@router.post('/', response_model=Book)
def create_book(book: BookCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO books (title, author_id, book_link, genres, average_rating, published_year) VALUES (?, ?, ?, ?, ?, ?)",
            (
                book.title,
                book.author_id,
                book.book_link,
                ",".join(book.genres) if book.genres else None,
                book.average_rating,
                book.published_year
            ))
        conn.commit()
        book_id = cursor.lastrowid
        return Book(id=book_id, *book.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The book with title {book.title} already exists."
        )
    finally:
        conn.close()

@router.put('/{book_id}', response_model=Book)
def update_book(
    book_id: int,
    book: BookCreate,
    _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    genres = ",".join(book.genres)
    cursor.execute(
        "UPDATE books SET title = ?, author_id = ?, book_link = ?, genres = ?, average_rating = ?, published_year = ? WHERE id = ?",
        (
            book.title,
            book.author_id,
            book.book_link,
            genres,
            book.average_rating,
            book.published_year,
            book_id
        )
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id '{book_id}' not found."
        )
    conn.commit()
    conn.close()
    return Book(id=book_id, *book.dict())

@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    conn.commit()
    conn.close()
    return {"detail: Book deleted!"}