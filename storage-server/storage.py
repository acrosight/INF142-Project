from pymongo import MongoClient

# Connecting to MongoDB
client = MongoClient(port=27017)
db = client.weather

class Meassurement(db.Meassurement):
    temperature = db.IntegerField()
    precipitation = db.IntegerField()
    location = db.StringField()