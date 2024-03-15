from flask import Flask, jsonify
from flask_cors import CORS
import requests

from database import MySQLConnection

app = Flask(__name__)
CORS(app)

mysql_connection = MySQLConnection(app, 'localhost', 'admin', 'admin', 'datadive')


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
    # checking dict keys match database column names
    # accounts_list = [{'id': account[0], 'name': account[1]} for account in accounts_list]
    return jsonify(accounts_list)


if __name__ == '__main__':
    app.run(debug=True)
