from models import Task,db
from flask import Blueprint,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required , get_jwt_identity
api=Api()
bcrypt = Bcrypt()


tasks_bp = Blueprint("tasks_bp",__name__)
api=Api(tasks_bp)



postings = reqparse.RequestParser()
postings.add_argument("Description",type = str,required = True ,help ="Enter the Description")


class Tasks(Resource):
    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        response = [task.to_dict() for task in tasks]
        return response, 200
   
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        Description = data.get('Description')

        if not Description:
            return jsonify({"error": "Missing description"}), 400

        new_task = Task(Description=Description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return {"message": "Task created successfully", "task": new_task.to_dict()}, 201
    
class TaskById(Resource):
    @jwt_required()
    def get(self,id):
        if id is None:
            tasks = Task.query.all()
            response = [tasks.to_dict() for user in tasks]
            return response, 200
        else:
            task = Task.query.get(id)
            if task:
                return task.to_dict(), 200
            else:
                return {"detail": "Task not found"}, 404
            
    @jwt_required()        
    def patch(self,id):
        task = Task.query.get(id)
        if not task:
            return {"detail": "Task not found"}, 404
        
        data = request.get_json()
        if 'Description' in data:
            task.Description = data['Description']
      
        db.session.commit()
        return task.to_dict(), 200
    
    @jwt_required()
    def delete(self,id):
        task = Task.query.get(id)
        if not task:
            return {"detail": "Task not found"}, 404
        
        db.session.delete(task)
        db.session.commit()
        return {"detail": "Task deleted"}, 200




api.add_resource(Tasks,"/tasks")
api.add_resource(TaskById,"/tasks/<int:id>")
