#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

#Root route
@app.route('/')
def hello_route():
    #function to display Hello HBNB
    return 'Hello HBNB!'

if __name__ == (__main__):
   app.run(port='3000', debug=True)
