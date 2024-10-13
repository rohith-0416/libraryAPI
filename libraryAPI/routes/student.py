from flask import Blueprint, jsonify, request
from models import Book, Student, Registration, db

student_bp = Blueprint('student', __name__)

#to get available books
@student_bp.route('/books', methods=['GET'])
def get_available_books():
    books = Book.query.filter(Book.available_copies > 0).all()
    return jsonify([{"title": book.title, "author": book.author, "copies": book.available_copies} for book in books])

#course registration
@student_bp.route('/register_course', methods=['POST'])
def register_course():
    student_id = request.json.get('student_id')
    course_name = request.json.get('course')
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    new_registration = Registration(student_id=student_id, course=course_name)
    db.session.add(new_registration)
    db.session.commit()

    return jsonify({"msg": "Course registered successfully"}), 201

#due date, due amount and borrowed list
@student_bp.route('/due_details', methods=['GET'])
def get_due_details_borrowedlist():
    student_id = request.args.get('student_id')  
    borrowed_books = Book.query.filter_by(borrowed_by=student_id, is_borrowed=True).all()

    if not borrowed_books:
        return jsonify({"msg": "No borrowed books found"}), 200

    due_details = []
    for book in borrowed_books:
        due_details.append({
            "book_title": book.title,
            "due_date": book.due_date,
            "due_amount": book.due_amount
        })

    return jsonify(due_details), 200
