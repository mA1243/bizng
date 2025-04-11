import mysql.connector 
import os

conn = mysql.connector.connect(
    host=os.getenv("MSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT")
)