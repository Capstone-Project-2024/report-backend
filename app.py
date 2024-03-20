from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_cors import CORS
import requests

from database import MySQLConnection

app = Flask(__name__)
CORS(app)

mysql_connection = MySQLConnection(app, 'localhost', 'admin', 'admin', 'datadive')

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    hashed_password = generate_password_hash(password)

    success = mysql_connection.insert_user(username, email, hashed_password)

    if success:
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user_verification = mysql_connection.verify_user(username, password)
    print(f"User verified: {user_verification}")

    if user_verification:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Incorrect username or password"}), 401

@app.route('/api/crypto')
def get_crypto_api_data():
    api_url = "https://api.coinlore.net/api/tickers/"
    response = requests.get(api_url)
    crypto = response.json()
    return jsonify(crypto)

@app.route('/accounts')
def index():
    cursor = mysql_connection.get_db().cursor()
    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()
    cursor.close()
    accounts_list = [dict(account) for account in accounts]
    return jsonify(accounts_list)


if __name__ == '__main__':
        app.run(debug=True)
