#!/usr/bin/python3
"""
Module for a basic Flask web application.

This script initializes a Flask server that listens for requests
on a specific port and returns a simple greeting.
"""

from flask import Flask

# Initialize the Flask application instance
# __name__ helps Flask determine the root path for resources
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """
    Handles requests to the root URL (/).

    Returns:
        str: A simple 'Hello HBNB!' greeting message.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Handles requests to the hbnb URL

    Returns:
        str: A simple 'HBNB' message.
    """
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Displays 'C ' followed by the value of the text variable.

    Args:
        text (str): The variable part of the URL. Underscores are
                   automatically replaced with spaces for readability.

    Returns:
        str: The formatted string 'C <text>'.
    """
    # Replacing underscores with spaces is standard for these web routes
    formatted_text = text.replace('_', ' ')
    return f"C {formatted_text}"


if __name__ == "__main__":
    """
    Main entry point of the script.

    Starts the Flask development server:
    - Host: Defaults to 127.0.0.1 (localhost)
    - Port: 3000
    - Debug: Enabled (provides detailed error messages and auto-reloads)
    """
    app.run(host='0.0.0.0', port=5000)
