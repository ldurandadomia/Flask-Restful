#!flask/bin/python
from authapp import app

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=7000)
