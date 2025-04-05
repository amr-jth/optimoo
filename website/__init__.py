from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_migrate import Migrate

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='na'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "na"  # Set a strong secret key!
    jwt = JWTManager(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')


    with app.app_context():
        db.create_all() 

    return app