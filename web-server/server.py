from flask import Flask, render_template
from util import dummy_data

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html', weather_data=dummy_data)

if __name__ == '__main__':
   app.run()


    