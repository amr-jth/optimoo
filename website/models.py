from .database import db

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  

    def __repr__(self):
        return f'<User {self.username}>'




class Cattle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=True)
    #photo = db.Column(db.String(200), nullable=True)  # Store only filename
    breed = db.Column(db.String(100), nullable=False)
    #gender = db.Column(db.String(20), nullable=False)
    life_stage = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    #birth_date = db.Column(db.Date, nullable=True)  #  Use Date instead of String
    weight = db.Column(db.Float, nullable=False)
    #height = db.Column(db.Float, nullable=True)
    feed_intake = db.Column(db.Float, nullable=False)
    feed_type = db.Column(db.String(50), nullable=True)
    health = db.Column(db.String(50), nullable=True)
    #notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Cattle {self.cattle_id} - {self.name}>"