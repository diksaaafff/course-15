from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Security Headers with Talisman
    talisman = Talisman(app)
    
    # Initialize CORS
    CORS(app)
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes
        db.create_all()
        
    return app
