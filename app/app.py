#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    return render_template('home.html')


if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000')
