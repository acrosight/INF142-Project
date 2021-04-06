import os

from flask import Flask, render_template
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

RUNNING_IN_DOCKER = True if os.environ.get('RUNNING_IN_DOCKER') else False

MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION')

URI = 'mongodb://root:example@localhost:27017/'
if RUNNING_IN_DOCKER:
    # Retrieves the variables necessary to assemble the MONGO URI
    URI = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:27017'

client = MongoClient(URI)
db = client[MONGODB_DATABASE]


@app.route('/')
def home_page():
    weather_data = list(db[MONGODB_COLLECTION].find(
        {}).sort('timestamp', DESCENDING).limit(100))
    return render_template('index.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
