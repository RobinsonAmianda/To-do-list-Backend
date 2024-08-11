from flask import request, Flask
from flask_restful import Resource, Api, reqparse
from models import User, db
from flask import Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token 
# from flask_login import LoginManager,logout_user


# login_manager = LoginManager()
# login_manager.init_app(app)
auth_bp = Blueprint("auth_bp", __name__)
api = Api(auth_bp)
bcrypt = Bcrypt()

register_parser = reqparse.RequestParser()
register_parser.add_argument("username", type=str, required=True, help="Enter the username")
register_parser.add_argument("email", type=str, required=True, help="Enter the email")
register_parser.add_argument("password", type=str, required=True, help="Enter the password")

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type=str, required=True, help="Enter the email")
login_parser.add_argument("password", type=str, required=True, help="Enter the password")

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not username or not email or not password:
            return {"detail": "All fields are required"}, 400

        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            return {"message": "Email already taken"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {
                "message": "User created successfully",
                "user" :new_user.to_dict()
                }, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return {"detail": "Both fields are required"}, 400

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                "detail":"User logged in successfully",
                "user":user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        else:
            return {"detail": "Invalid email or password"}, 401


# class Logout(Resource):
#     def post(self):
#         logout_user()
#         return {"detail":"Logout successfully"}, 200

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
# api.add_resource(Logout, "/logout")