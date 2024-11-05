#!/usr/bin/python3
"""Flask app"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render a html template"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
