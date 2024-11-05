#!/usr/bin/python3
"""Babel setup"""
from flask import Flask, render_template, request
from flask_babel import Babel
from typing import List

# Flask app instance
app = Flask(__name__)

# Instantiate Babel
babel = Babel(app)

class Config:
    """Configuration app class"""
    LANGUAGES: List[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = 'en'
    BABEL_DEFAULT_TIMEZONE: str = 'UTC'

# Set the app configuration
app.config.from_object(Config)

@babel.localeselector
def get_locale() -> str:
    """
    This function is called by Flask-Babel to determine the best locale
    for the current request. It uses the `Accept-Language` header from
    the request and selects the best match from the supported languages.
    """
    # Use the `request.accept_languages` object to get the list of accepted languages.
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/', strict_slashes=False)
def index() -> str:
    """Render an HTML template"""
    return render_template('2-index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

