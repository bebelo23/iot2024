from dotenv import load_dotenv
load_dotenv()

from collections import OrderedDict
from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return [
        OrderedDict([
            ('id', book.id),
            ('title', book.title),
            ('author', book.author),
            ('year', book.year),
            ('is_published', book.is_published)
        ]) for book in books
    ]

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        return OrderedDict([
            ('id', book.id),
            ('title', book.title),
            ('author', book.author),
            ('year', book.year),
            ('is_published', book.is_published)
        ])
    return {'message': 'Book not found'}

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return OrderedDict([
        ('id', newbook.id),
        ('title', newbook.title),
        ('author', newbook.author),
        ('year', newbook.year),
        ('is_published', newbook.is_published)
    ])

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        return {'message': 'Data Not Found'}
    for key, value in book.items():
        if key in ['title', 'author', 'year', 'is_published']:
            setattr(existing_book, key, value)
    db.commit()
    db.refresh(existing_book)
    return OrderedDict([
        ('id', existing_book.id),
        ('title', existing_book.title),
        ('author', existing_book.author),
        ('year', existing_book.year),
        ('is_published', existing_book.is_published)
    ])

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        return {'message': 'Data Not Found'}
    db.delete(existing_book)
    db.commit()
    return {"detail": "Book deleted successfully"}


#student part 
@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return [
        OrderedDict([
            ('id', student.id),
            ('Fname', student.Fname),
            ('Lname', student.Lname),
            ('Std_numid', student.Std_numid),
            ('birth', student.birth),
            ('gender', student.gender)
        ]) for student in students
    ]

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        return OrderedDict([
            ('id', student.id),
            ('Fname', student.Fname),
            ('Lname', student.Lname),
            ('Std_numid', student.Std_numid),
            ('birth', student.birth),
            ('gender', student.gender)
        ])
    return {'message': 'Student not found'}

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    new_student = models.Student(
        Fname=student['Fname'],
        Lname=student['Lname'],
        Std_numid=student['Std_numid'],
        birth=student['birth'],
        gender=student['gender']
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    response.status_code = 201
    return OrderedDict([
        ('id', new_student.id),
        ('Fname', new_student.Fname),
        ('Lname', new_student.Lname),
        ('Std_numid', new_student.Std_numid),
        ('birth', new_student.birth),
        ('gender', new_student.gender)
    ])

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not existing_student:
        return {'message': 'Student not found'}
    for key, value in student.items():
        if key in ['Fname', 'Lname', 'Std_numid', 'birth', 'gender']:
            setattr(existing_student, key, value)
    db.commit()
    db.refresh(existing_student)
    return OrderedDict([
        ('id', existing_student.id),
        ('Fname', existing_student.Fname),
        ('Lname', existing_student.Lname),
        ('Std_numid', existing_student.Std_numid),
        ('birth', existing_student.birth),
        ('gender', existing_student.gender)
    ])

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not existing_student:
        return {'message': 'Student not found'}
    db.delete(existing_student)
    db.commit()
    return {"detail": "Student deleted successfully"}




app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
