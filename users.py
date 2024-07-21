from models import User,db
from flask import Blueprint ,jsonify , request
from flask_restful import Resource,Api,reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required , get_jwt_identity
api=Api()
bcrypt = Bcrypt()


users_bp = Blueprint("users_bp",__name__)
api=Api(users_bp)



updates = reqparse.RequestParser()
updates.add_argument("username",type = str,help ="Enter the username")
updates.add_argument("email",type = str,help ="Enter the email")
updates.add_argument("password",type = str,help ="Enter the password")


class Users(Resource):
    @jwt_required() 
    def get(self):
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return response, 200


class UserById(Resource):
    @jwt_required() 
    def get(self, id=None):
        if id is None:
            users = User.query.all()
            response = [user.to_dict() for user in users]
            return response, 200
        else:
            user = User.query.get(id)
            if user:
                return user.to_dict(), 200
            else:
                return {"detail": "User not found"}, 404
            
    @jwt_required()         
    def patch(self,id):
        user = User.query.get(id)
        if not user:
            return {"detail": "User not found"}, 404
        
        data = request.get_json()
        user.username = data.get('username',user.username)
        user.email = data.get('email',user.email)
        user.password = data.get('password',user.password)
        
        db.session.commit()
        return user.to_dict(), 200
    
    @jwt_required()  
    def delete(self,id):
        user = User.query.get(id)
        if not user:
            return {"detail": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {"detail": "User deleted"}, 200




api.add_resource(Users,"/users")
api.add_resource(UserById,"/users/<int:id>")
