from flask import Flask, jsonify
from flask_cors import CORS

from database import MySQLConnection

app = Flask(__name__)
CORS(app)

mysql_connection = MySQLConnection(app, 'localhost', 'admin', 'admin', 'datadive')


@app.route('/')

def index():

    cursor = mysql_connection.get_db().cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    users_list = [dict(user) for user in users]
    return jsonify(users_list)


if __name__ == '__main__':
    app.run(debug=True)
