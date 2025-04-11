from flask import Flask
from flask_migrate import Migrate
import os
import dotenv
import mysql.connector

dotenv.load_dotenv()

def create_app():
    
    from bizng.models import db
    from bizng.db import conn
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    
    app.config["MYSQL_CONN"] = conn = mysql.connector.connect(
    host=os.getenv("MSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT")
)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()

from bizng import routes