#!/usr/bin/python3
"""Babel setup"""
from flask import Flask, render_template
from flask_babel import Babel
from typing import List


#Flask app instance
app = Flask(__name__)


#Instantiate Babel
babel = Babel


class Config():
    """Configuration app class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = 'en'
    BABEL_DEFAULT_TIMEZONE: str = 'UTC'


app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render a html template"""
    return render_template('1-index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
