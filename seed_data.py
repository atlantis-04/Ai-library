from library_manager import LibraryManager
from datetime import datetime, timedelta
import random

def seed_database():
    """Populate database with sample data"""
    manager = LibraryManager()
    
    # Add members
    members = [
        ("Alice Johnson", "alice@email.com"),
        ("Bob Smith", "bob@email.com"),
        ("Carol White", "carol@email.com"),
        ("David Brown", "david@email.com"),
        ("Emma Davis", "emma@email.com"),
        ("Frank Wilson", "frank@email.com"),
        ("Grace Lee", "grace@email.com"),
        ("Henry Taylor", "henry@email.com")
    ]
    
    member_ids = []
    for name, email in members:
        try:
            mid = manager.add_member(name, email)
            member_ids.append(mid)
        except:
            pass
    
    # Add books
    books = [
        ("The Martian", "Andy Weir", "Science Fiction", "978-0553418026", 3),
        ("Sapiens", "Yuval Noah Harari", "History", "978-0062316097", 2),
        ("Clean Code", "Robert Martin", "Technology", "978-0132350884", 2),
        ("1984", "George Orwell", "Fiction", "978-0451524935", 4),
        ("Cosmos", "Carl Sagan", "Science", "978-0345539434", 2),
        ("The Pragmatic Programmer", "Andrew Hunt", "Technology", "978-0135957059", 2),
        ("Dune", "Frank Herbert", "Science Fiction", "978-0441172719", 3),
        ("Educated", "Tara Westover", "Biography", "978-0399590504", 2),
        ("Atomic Habits", "James Clear", "Self-Help", "978-0735211292", 3),
        ("The Design of Everyday Things", "Don Norman", "Design", "978-0465050659", 2),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", "978-0374533557", 2),
        ("The Lean Startup", "Eric Ries", "Business", "978-0307887894", 2),
        ("Neuromancer", "William Gibson", "Science Fiction", "978-0441569595", 2),
        ("A Brief History of Time", "Stephen Hawking", "Science", "978-0553380163", 2),
        ("The Phoenix Project", "Gene Kim", "Technology", "978-0988262508", 2)
    ]
    
    book_ids = []
    for title, author, genre, isbn, copies in books:
        try:
            bid = manager.add_book(title, author, genre, isbn, copies)
            book_ids.append(bid)
        except:
            pass
    
    # Create sample transactions
    if member_ids and book_ids:
        for _ in range(30):
            member_id = random.choice(member_ids)
            book_id = random.choice(book_ids)
            success, msg = manager.borrow_book(member_id, book_id)
            
            if success:
                transactions = manager.get_all_transactions()
                if not transactions.empty:
                    last_trans = transactions.iloc[-1]
                    if random.random() > 0.3:
                        manager.return_book(last_trans['id'])
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
