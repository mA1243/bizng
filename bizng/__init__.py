from flask import Flask
from flask_migrate import Migrate

def create_app():
    
    from bizng.models import db
    from bizng.db import conn
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()

from bizng import routes