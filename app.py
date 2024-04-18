from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from stocksymbol import StockSymbol
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


@app.route('/accounts')
def index():
    cursor = mysql_connection.get_db().cursor()
    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()
    cursor.close()
    accounts_list = [dict(account) for account in accounts]
    return jsonify(accounts_list)


@app.route('/api/crypto')
def get_crypto_api_data():
    api_url = "https://api.coinlore.net/api/tickers/"
    response = requests.get(api_url)
    crypto = response.json()
    return jsonify(crypto)


@app.route('/api/currencyExchange', methods=['GET', 'POST'])
def make_currency_exchange_list():
    if request.method == 'POST':
        currency_want = request.json['wanted_Currency']
        currency_have = request.json['starting_currency']
        amount = request.json['currency_Amount']

        urls = 'https://api.api-ninjas.com/v1/convertcurrency?want={}&have={}&amount={}'.format(currency_want,
                                                                                                currency_have, amount)
        response = requests.get(urls, headers={'X-Api-Key': '1CVkczf/+3vz6KBha/rZQw==ifMPWZGqaDOIBRAq'})
        top_currency_exchanges = response.json()
        return jsonify(top_currency_exchanges)
    else:

        return jsonify({})


@app.route('/api/stockMarket')
def get_stock_symbol_list():
    api_key = "d2a135e4-14b7-4040-81e2-563977ca843c"
    stock_market = StockSymbol(api_key)
    market_list = stock_market.get_symbol_list(index="SPX")

    return jsonify(market_list)


@app.route('/api/stockMarketValues', methods=['POST'])
def get_stock_market_values():
    symbol = request.json['tickerSymbol']
    api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
    api_key = "6kMXQ19jn+NsXydcrpXacQ==H4uMv3RaOjIJovI6"
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    stock_price = response.json()

    return jsonify(stock_price)


if __name__ == '__main__':
    app.run(debug=True)
