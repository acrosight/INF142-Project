import os

from datetime import datetime
from flask import Flask, render_template
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)


MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', "root")
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', "example")
MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME', "localhost")
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', "weatherstation")
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION', "sensorData")

# Retrieves the variables necessary to assemble the MONGO URI
URI = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:27017'

client = MongoClient(URI)
db = client[MONGODB_DATABASE]

@app.template_filter('datetimeformat')
def datetimeformat(s):
    dt_object = datetime.fromtimestamp(s)
    date_time = dt_object.strftime("%d/%m/%Y, %H:%M")
    return date_time


@app.route('/')
def home_page():
    weather_data = list(db[MONGODB_COLLECTION].find(
        {}).sort('timestamp', DESCENDING))
    return render_template('index.html', weather_data=weather_data)


app.jinja_env.filters['datetimeformat'] = datetimeformat


if __name__ == '__main__':
    app.run(host="0.0.0.0")