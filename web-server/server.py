from flask import Flask, render_template
from flask_mongoengine import MongoEngine

from util import dummy_data

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'weatherstation',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

# TODO: Add Weather Data Model

# TODO: Add Endpoints for creating weather data rows.


class WeatherMeasurement(db.Document):
    pass


@app.route('/api/measurement', methods=['POST', 'DELETE'])
def measurement(request):
    if request.method == 'POST':
        # Add measurement
        pass
    if request.method == 'DELETE':
        # Delete measurement
        pass


@app.route('/')
def home_page():
    return render_template('index.html', weather_data=dummy_data)


if __name__ == '__main__':
    app.run()
