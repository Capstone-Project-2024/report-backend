from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


def get_data():
    return jsonify({'message': 'test connection for weekly report screenshot'})


if __name__ == '__main__':
    app.run(debug=True)
