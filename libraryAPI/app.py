from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#importing routes as blueprints
from config import Config
from models import db
from routes.student import student_bp
from routes.admin import admin_bp

#initialize Flask app and extensions 
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

#register blueprints for different route modules
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)

#running the app
if __name__ == '__main__':
    app.run(debug=True)
