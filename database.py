from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


class MySQLConnection:
    def __init__(self, app=None, host='localhost', user='your_username', password='your_password', dbname='datadive'):
        if app is not None:
            self.init_app(app, host, user, password, dbname)

    def init_app(self, app, host, user, password, dbname):
        # Set up database configurations directly within the class
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = dbname
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Optional: Use DictCursor to return results as dictionaries
        self.mysql = MySQL(app)

    def get_db(self):
        return self.mysql.connection
