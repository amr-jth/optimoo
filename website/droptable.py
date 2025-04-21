from website import create_app
from website.database import db
from website.models import Cattle,User,FeedRecord  # Ensure this is the correct import path

app = create_app()  # Create the Flask app

# Run the table drop inside the application context
with app.app_context():
    FeedRecord.__table__.drop(db.engine)

    print("Cattle table dropped successfully!")
