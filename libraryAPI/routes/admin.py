from flask import Blueprint, jsonify, request
from models import Book, Student, Registration, db

admin_bp = Blueprint('admin', __name__)

#adding book
@admin_bp.route('/books', methods=['POST'])
def add_book():
    title = request.json.get('title')
    author = request.json.get('author')
    copies = request.json.get('available_copies')

    new_book = Book(title=title, author=author, available_copies=copies)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"msg": "Book added successfully"}), 201

#adding student 
@admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    student.name = request.json.get('name', student.name)
    student.email = request.json.get('email', student.email)
    db.session.commit()

    return jsonify({"msg": "Student details updated"}), 200


#deleting book
@admin_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"msg": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()

    return jsonify({"msg": "Book deleted successfully"}), 200


#deleting student registration
@admin_bp.route('/registrations/<int:registration_id>', methods=['DELETE'])
def delete_registration(registration_id):
    registration = Registration.query.get(registration_id)
    if not registration:
        return jsonify({"msg": "Registration not found"}), 404
    db.session.delete(registration)
    db.session.commit()

    return jsonify({"msg": "Registration deleted successfully"}), 200


#checking for borrowed books
@admin_bp.route('/borrowed-books', methods=['GET'])
def borrowed_books():
    borrowed_books = Book.query.filter_by(is_borrowed=True).all()

    if not borrowed_books:
        return jsonify({"msg": "No books are currently borrowed"}), 200

    result = []
    for book in borrowed_books:
        borrower = Student.query.get(book.borrowed_by)  
        result.append({
            "book_title": book.title,
            "book_author": book.author,
            "borrower_name": borrower.name if borrower else "Unknown",
            "borrower_email": borrower.email if borrower else "Unknown",
            "due_date": book.due_date,
            "due_amount": book.due_amount
        })

    return jsonify(result), 200

