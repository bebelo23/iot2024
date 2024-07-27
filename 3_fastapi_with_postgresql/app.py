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

#coffee part
@router_v1.get('/coffees')
async def get_coffee(db: Session = Depends(get_db)):
    return db.query(models.Coffee).all()

@router_v1.get('/coffees/{coffee_id}')
async def get_coffee(coffee_id: int, db: Session = Depends(get_db)):
    return db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()

@router_v1.post('/coffees')
async def create_coffee(coffee: dict, response: Response, db: Session = Depends(get_db)):
    new_coffee = models.Coffee(name=coffee['name'], description=coffee['description'], price=coffee['price'])
    db.add(new_coffee)
    db.commit()
    db.refresh(new_coffee)
    response.status_code = 201
    return new_coffee

@router_v1.patch('/coffees/{coffee_id}')
async def update_coffee(coffee_id: int, coffee: dict, db: Session = Depends(get_db)):
    existing_coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not existing_coffee:
        return {
        'message': 'coffee not found'
    }
    if 'name' in coffee:
        existing_coffee.name = coffee['name']
    if 'description' in coffee:
        existing_coffee.description = coffee['description']
    if 'price' in coffee:
        existing_coffee.price = coffee['price']
    db.commit()
    db.refresh(existing_coffee)
    return existing_coffee

@router_v1.delete('/coffees/{coffee_id}')
async def delete_coffee(coffee_id: int, db: Session = Depends(get_db)):
    existing_coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not existing_coffee:
        return {
        'message': 'coffee not found'
    }
    db.delete(existing_coffee)
    db.commit()
    return {"detail": "coffee deleted successfully"}

#orders part
@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    new_order = models.Order(coffee_id=order['coffee_id'], quantity=order['quantity'], total_price=order['total_price'], notes=order['notes'])
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    response.status_code = 201
    return new_order

@router_v1.patch('/orders/{order_id}')
async def update_order(response: Response ,order_id: int, order: dict, db: Session = Depends(get_db),):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for key, value in order.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        return response.status_code == 404

@router_v1.delete('/orders/{order_id}')
async def delete_order(response: Response, order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return {"message": "Order deleted successfully"}
    else:
        return response.status_code == 404



app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
