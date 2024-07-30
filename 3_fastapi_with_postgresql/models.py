from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    detail = Column(String, index=True)
    synopsis = Column(String, index=True)
    category = Column(String, index=True)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    Fname = Column(String, index=True)
    Lname = Column(String,index=True)
    Std_numid = Column(Integer, index=True)
    birth = Column(String, index=True)
    gender = Column(String, index=True)

class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    quantity = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    notes = Column(String, index=True)
