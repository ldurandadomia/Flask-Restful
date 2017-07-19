#!flask/bin/python
from flask import Flask, jsonify
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

