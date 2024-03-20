from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash

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

    def verify_user(self, username, password):
        cursor = self.get_db().cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user['password'], password):
            return True
        return False

    def insert_user(self, username, email, hashed_password):
        cursor = self.get_db().cursor()
        try:
            cursor.execute('INSERT INTO account (username, email, password) VALUES (%s, %s, %s)',
                           (username, email, hashed_password))
            self.get_db().commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            cursor.close()
