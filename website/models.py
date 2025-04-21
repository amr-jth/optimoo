from .database import db
from datetime import datetime

# class User(db.Model):  
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)  

#     def __repr__(self):
#         return f'<User {self.username}>'


class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    contact=db.Column(db.String(200),nullable=True, unique=True)
    location=db.Column(db.String(100),nullable=True)
    size=db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'




class Cattle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=True)
    type=db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(200), nullable=False)  # Store only filename
    breed = db.Column(db.String(100), nullable=False)
    life_stage = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    feed_intake = db.Column(db.Float, nullable=False)
    feed_type = db.Column(db.String(50), nullable=True)
    health = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Cattle {self.cattle_id} - {self.name}>"






class FeedRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    cow_type = db.Column(db.String(50))
    weight = db.Column(db.Float)
    milk_yield = db.Column(db.Float)
    feed_type = db.Column(db.String(50))
    optimized_feed = db.Column(db.Text)
    total_cost = db.Column(db.Float)
    dmi_gap = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Float)
    weight = db.Column(db.Float)
    milk_yield = db.Column(db.Float)
    bcs = db.Column(db.Float)
    market_ready = db.Column(db.String(10))
    predicted_days = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
