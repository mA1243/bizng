from flask import Flask
from flask_migrate import Migrate
import os
import mysql.connector

def create_app():
    
    from bizng.models import db
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    
    app.config["MYSQL_CONN"] = conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT") or 3306)
)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()

from bizng import routes