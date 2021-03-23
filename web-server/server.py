# TODO: Import MongoDB
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


# TODO: Serve static files from frontend folder

# TODO: Add API endpoint for serving weather data from mongodb.