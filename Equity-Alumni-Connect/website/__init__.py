from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import create_engine
from flask_migrate import Migrate
from builtins import zip


password='test%401234'
admin_name = 'milton'
uri = f'postgresql+psycopg2://milton:{password}@elp-server.postgres.database.azure.com/postgres?sslmode=require'
# uri = f'postgresql+psycopg2://{admin_name}:{password}@elpserver.postgres.database.azure.com/postgres?sslmode=require'
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='mrcaptain@12345.vectorized.ithinkthisisverystrongforasecuritykey',
        SQLALCHEMY_DATABASE_URI=uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix='/auth')

    from .models import User, Note

    with app.app_context():
        db.create_all() # use db.drop_all() to drop all tables

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    migrate = Migrate(app, db)
    
    # Define a function to pass as a global variable to Jinja2    
    def jinja2_zip(*args):
        return zip(*args)
    
    # Add the zip function to the Jinja2 global variables
    app.jinja_env.globals.update(zip=jinja2_zip)
    
    return app

