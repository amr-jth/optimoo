from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import db
from flask_migrate import Migrate

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='na'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')


    with app.app_context():
        db.create_all() 

    return app