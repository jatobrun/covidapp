from flask import Flask
from pymongo import MongoClient
from pathlib import Path
from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c81dac792846c247acb200f1b0a7eab4'
client = MongoClient("mongodb+srv://jatobrun:jatobrun@cluster0-hx8rh.mongodb.net/test?retryWrites=true&w=majority")
db = client['Covid']
tabla_pacientes = db['Pacientes']
tabla_usuarios = db['Usuarios']
bcrypt = Bcrypt(app)
from src import routes
