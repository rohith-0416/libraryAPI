from models import Book, db, Admin

class LibraryService:
    
    @staticmethod
    def add_new_book(admin_id, title, author, available_copies):
        admin = Admin.query.get(admin_id)
        if not admin:
            return {"msg": "Unauthorized"}, 401  

        if not title or not author or available_copies is None:
            return {"msg": "Missing required fields"}, 400

        new_book = Book(title=title, author=author, available_copies=available_copies)
        db.session.add(new_book)
        db.session.commit()

        return {"msg": "Book added successfully"}, 201

    @staticmethod
    def update_book_info(admin_id, book_id, data):
        admin = Admin.query.get(admin_id)
        if not admin:
            return {"msg": "Unauthorized"}, 401  

        book = Book.query.get(book_id)
        if not book:
            return {"msg": "Book not found"}, 404

        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.available_copies = data.get('available_copies', book.available_copies)
        
        db.session.commit()
        return {"msg": "Book updated successfully"}, 200

    @staticmethod
    def borrow_book(book_id, student_id):
        book = Book.query.get(book_id)
        if not book or book.available_copies <= 0:
            return {"msg": "Book not available"}, 400

        book.available_copies -= 1
        book.student_id = student_id
        db.session.commit()

        return {"msg": "Book borrowed successfully"}, 200

    @staticmethod
    def return_book(book_id):
        book = Book.query.get(book_id)
        if not book or not book.student_id:
            return {"msg": "This book is not borrowed"}, 400

        book.available_copies += 1
        book.student_id = None
        db.session.commit()

        return {"msg": "Book returned successfully"}, 200
