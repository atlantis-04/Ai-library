from models import Session, Member, Book, Transaction
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import func

class LibraryManager:
    def __init__(self):
        self.session = Session()
        self.fine_per_day = 2.0
        self.max_borrow_days = 14
        self.max_books_per_member = 3
    
    def add_member(self, name, email):
        """Register a new member"""
        member = Member(name=name, email=email)
        self.session.add(member)
        self.session.commit()
        return member.id
    
    def add_book(self, title, author, genre, isbn, copies=1):
        """Add a new book to library"""
        book = Book(title=title, author=author, genre=genre, isbn=isbn, 
                   total_copies=copies, available_copies=copies)
        self.session.add(book)
        self.session.commit()
        return book.id
    
    def borrow_book(self, member_id, book_id):
        """Process book borrowing"""
        member = self.session.query(Member).filter_by(id=member_id).first()
        book = self.session.query(Book).filter_by(id=book_id).first()
        
        if not member or not book:
            return False, "Member or Book not found"
        
        if not member.is_active:
            return False, "Member account is inactive"
        
        active_borrows = self.session.query(Transaction).filter_by(
            member_id=member_id, status='borrowed'
        ).count()
        
        if active_borrows >= self.max_books_per_member:
            return False, f"Maximum {self.max_books_per_member} books allowed"
        
        if book.available_copies <= 0:
            return False, "Book not available"
        
        due_date = datetime.now() + timedelta(days=self.max_borrow_days)
        transaction = Transaction(
            member_id=member_id,
            book_id=book_id,
            due_date=due_date,
            status='borrowed'
        )
        
        book.available_copies -= 1
        book.available = book.available_copies > 0
        
        self.session.add(transaction)
        self.session.commit()
        return True, "Book borrowed successfully"
    
    def return_book(self, transaction_id):
        """Process book return and calculate fine"""
        transaction = self.session.query(Transaction).filter_by(id=transaction_id).first()
        
        if not transaction or transaction.status == 'returned':
            return False, "Invalid transaction"
        
        transaction.return_date = datetime.now()
        transaction.status = 'returned'
        
        if transaction.return_date > transaction.due_date:
            days_late = (transaction.return_date - transaction.due_date).days
            transaction.fine = days_late * self.fine_per_day
            
            member = self.session.query(Member).filter_by(id=transaction.member_id).first()
            member.total_fines += transaction.fine
        
        book = self.session.query(Book).filter_by(id=transaction.book_id).first()
        book.available_copies += 1
        book.available = True
        
        self.session.commit()
        return True, f"Book returned. Fine: ${transaction.fine:.2f}"
    
    def get_all_members(self):
        """Get all members as DataFrame"""
        members = self.session.query(Member).all()
        return pd.DataFrame([{
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'join_date': m.join_date,
            'total_fines': m.total_fines,
            'is_active': m.is_active
        } for m in members])
    
    def get_all_books(self):
        """Get all books as DataFrame"""
        books = self.session.query(Book).all()
        return pd.DataFrame([{
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'genre': b.genre,
            'isbn': b.isbn,
            'total_copies': b.total_copies,
            'available_copies': b.available_copies,
            'available': b.available
        } for b in books])
    
    def get_all_transactions(self):
        """Get all transactions as DataFrame"""
        transactions = self.session.query(Transaction).all()
        return pd.DataFrame([{
            'id': t.id,
            'member_id': t.member_id,
            'book_id': t.book_id,
            'borrow_date': t.borrow_date,
            'due_date': t.due_date,
            'return_date': t.return_date,
            'fine': t.fine,
            'status': t.status
        } for t in transactions])
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        total_books = self.session.query(Book).count()
        total_members = self.session.query(Member).filter_by(is_active=True).count()
        borrowed_books = self.session.query(Transaction).filter_by(status='borrowed').count()
        total_fines = self.session.query(func.sum(Member.total_fines)).scalar() or 0
        
        return {
            'total_books': total_books,
            'total_members': total_members,
            'borrowed_books': borrowed_books,
            'total_fines': total_fines
        }
