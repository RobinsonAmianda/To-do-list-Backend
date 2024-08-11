import os
from flask import Flask 
from tasks import tasks_bp
from users import users_bp
from models import db, User  
from auth import auth_bp
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_login import LoginManager, logout_user

app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

api = Api(app)
jwt = JWTManager(app)

class Logout(Resource):
    def post(self):
        logout_user()
        return {"detail": "Logout successfully"}, 200

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('Database') 
app.config['JWT_SECRET_KEY'] = os.environ.get('Secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(tasks_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

api.add_resource(Logout, "/logout")

if __name__ == "__main__": 
    app.run(debug=True)
