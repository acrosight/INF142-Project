import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient, DESCENDING
from bson import json_util
import json

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
    '''
    Flask filter for formatting ISO date string to user friendly dateTime
    '''
    dt_object = datetime.fromisoformat(s)
    date_time = dt_object.strftime("%d/%m/%Y, %H:%M")
    return date_time


# Dynamic page load rendered by flask
@app.route('/')
def home_page():
    weather_data = list(db[MONGODB_COLLECTION]
                        .find({})
                        .sort('timestamp', DESCENDING)
                        .limit(100)
                        )
    return render_template('index.html', weather_data=weather_data)


# Rest api
@app.route('/api/data')
def get_weather_data():
    '''
    Get weather data from MongoDB based on location in http query

    ex: GET localhost:5000/api/data?location=Bergen&limit=100

    ^^-> Will return latest 100 records from Bergen
    '''
    limit = int(request.args.get('limit', '100'))
    location = request.args.get('location', None)

    # Build MongoDB query
    query = {}
    if location is not None:
        query['location'] = location

    weather_data = list(db[MONGODB_COLLECTION]
                        .find(query)
                        .sort('timestamp', DESCENDING)
                        .limit(limit)
                        )

    # convert bson from mongodb to json string
    # Required since mongodb returns ObjectId type for id which is not parseable to json
    json_string = json.loads(json_util.dumps(weather_data))

    # Convert to appropiate json for sending over http
    # Includes setting the http header to application/json
    return jsonify(json_string)


@app.route('/api/location')
def get_locations():
    '''
        Return a list of all unique locations in mongodb
    '''
    locations = list(db[MONGODB_COLLECTION]
                     .find({})
                     .distinct('location')
                     )

    # convert bson from mongodb to json string
    json_string = json.loads(json_util.dumps(locations))

    # Convert to appropiate json for sending over http
    return jsonify(json_string)


app.jinja_env.filters['datetimeformat'] = datetimeformat


# On application load, start listening on 0.0.0.0 (localhost and global internet)
if __name__ == '__main__':
    app.run(host="0.0.0.0")
