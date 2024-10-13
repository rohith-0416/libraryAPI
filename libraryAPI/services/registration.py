from models import Student, Registration, db

class RegistrationService:
    @staticmethod
    def register_student_for_course(data):
        validation_error = RegistrationService.validate_registration_data(data)
        if validation_error:
            return validation_error

        student_id = data['student_id']
        course = data['course'] 

        student = Student.query.get(student_id)
        if not student:
            return {"msg": "Student not found"}, 404

        
        existing_registration = Registration.query.filter_by(student_id=student_id, course=course).first()
        if existing_registration:
            return {"msg": "Student is already registered for this course"}, 400

        
        new_registration = Registration(student_id=student_id, course=course)

        db.session.add(new_registration)
        db.session.commit()

        return {"msg": "Registration successful", "registration_id": new_registration.id}, 200

    @staticmethod
    def validate_registration_data(data):
        required_fields = ['student_id', 'course']
        for field in required_fields:
            if field not in data:
                return {"msg": f"{field} is required"}, 400
        return None
