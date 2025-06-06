from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:projetinhos2025@db:3306/quiosque_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    db.init_app(app)

    return app
