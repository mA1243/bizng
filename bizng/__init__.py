from flask import Flask
from flask_migrate import Migrate

import pymysql
pymysql.install_as_MySQLdb()

def create_app():
    
    from bizng.models import db
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()

from bizng import routes
