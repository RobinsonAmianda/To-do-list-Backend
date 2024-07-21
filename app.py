import os
from flask import Flask 
from tasks import *
from users import *
from models import *
from auth import *
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)

api = Api()
jwt = JWTManager(app)

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

if __name__ == "__main__": 
	app.run(debug=True) 
