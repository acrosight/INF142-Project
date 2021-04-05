import os

from flask import Flask, render_template
from flask_pymongo import PyMongo

from util import dummy_data

app = Flask(__name__)

# Retrieves the variables necessary to assemble the MONGO URI
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')

app.config["MONGO_URI"] = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}' \
    '@{MONGODB_HOSTNAME}:27017/{MONGODB_DATABASE}'

# Instantiates the connection to the database.
mongo = PyMongo(app)
db = mongo.db


@app.route('/')
def home_page():
    return render_template('index.html', weather_data=dummy_data)


if __name__ == '__main__':
    app.run()
