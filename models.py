from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

 
class User(db.Model,SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String , nullable = False)
    email = db.Column(db.String , nullable = False,unique =True)
    password = db.Column(db.String , nullable = False)
    tasks = db.relationship("Task" , backref= "users")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "tasks":self.tasks
        }


class Task(db.Model,SerializerMixin):
    __tablename__ = "tasks"
    id = db.Column(db.Integer , primary_key = True)
    Description = db.Column(db.String , nullable = False)
    user_id = db.Column(db.Integer ,ForeignKey("users.username"),nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "Description": self.Description,
            "user": self.user_id
        }