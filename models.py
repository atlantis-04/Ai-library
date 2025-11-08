from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    join_date = Column(DateTime, default=datetime.now)
    total_fines = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    transactions = relationship('Transaction', back_populates='member')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    isbn = Column(String, unique=True)
    available = Column(Boolean, default=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    transactions = relationship('Transaction', back_populates='book')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    fine = Column(Float, default=0.0)
    status = Column(String, default='borrowed')
    member = relationship('Member', back_populates='transactions')
    book = relationship('Book', back_populates='transactions')

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
