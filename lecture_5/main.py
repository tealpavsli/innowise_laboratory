from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import BookCreate, Book, BookUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ▶ Create (POST)
@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# ▶ Read all (GET)
@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


# ▶ Delete (DELETE)
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# ▶ Update (PUT)
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


# ▶ Search endpoint
@app.get("/books/search/", response_model=list[Book])
def search_books(title: str | None = None,
                 author: str | None = None,
                 year: int | None = None,
                 db: Session = Depends(get_db)):

    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(models.Book.year == year)

    return query.all()
