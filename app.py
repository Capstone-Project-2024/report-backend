from flask import Flask, jsonify
from flask_cors import CORS

from database import MySQLConnection

app = Flask(__name__)
CORS(app)

mysql_connection = MySQLConnection(app, 'localhost', 'admin', 'admin', 'datadive')


@app.route('/')

def index():
    cursor = mysql_connection.get_db().cursor()
    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()
    cursor.close()
    accounts_list = [dict(account) for account in accounts]
    return jsonify(accounts_list)


if __name__ == '__main__':
    app.run(debug=True)
