# Importing necessary modules and Libraries
import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from flask_migrate import Migrate
from builtins import zip
from dotenv import load_dotenv

# load environment variables
load_dotenv()
# NOTE: in production the password and admin name are stored in the .env file I have provided the credentials here in the url so that the appp runs on any test computer
# password=os.getenv("PASSWORD")
# admin_name = os.getenv("ADMIN_NAME")
# uri = f'postgresql+psycopg2://{admin_name}:{password}@elp-server.postgres.database.azure.com/postgres?sslmode=require'
uri = f'postgresql+psycopg2://milton:test%401234@elp-server.postgres.database.azure.com/postgres?sslmode=require'
# secret_key = os.getenv("SECRET_KEY")
db = SQLAlchemy()

# Function to create Flask app instance
def create_app():
    app = Flask(__name__) # Creating Flask app instance
    
    # Setting configuration parameters
    app.config.from_mapping(
        SECRET_KEY='cqoihrn08984h8crnejwcjanal89qrfh710rnqp1ch7rbo6dvb',  # A secret key for securely signing session cookies and other security-related needs
        SQLALCHEMY_DATABASE_URI=uri, # The URI for accessing the PostgreSQL database
        SQLALCHEMY_TRACK_MODIFICATIONS=True  # Enables tracking modifications for SQLAlchemy, could be set to False incase of perfomance issues
    )
    
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app

    # Importing views and auth blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views) # Registering the views blueprint
    app.register_blueprint(auth, url_prefix='/auth')# Registering the auth blueprint with a prefix URL   
    app.register_blueprint(admin, url_prefix='/admin')# Registering the auth blueprint with a prefix URL   
    

    from .models import User, AlumniScholarProfiles

    with app.app_context():
        # Creating all tables in the database using the defined models. Use db.drop_all() to drop all tables
        db.create_all()  
        
    # Initializing admin login and setting the login view
    admin_login_manager = LoginManager()
    admin_login_manager.login_view = 'admin.login'
    admin_login_manager.init_app(app)

    @admin_login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # Initializing Flask-Login and setting the login view
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Defining a function to load user with the given ID from the database
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Initializing Flask-Migrate
    migrate = Migrate(app, db)
    
    # Define a function to pass as a global variable to Jinja2    
    def jinja2_zip(*args):
        return zip(*args)
    
    # Add the zip function to the Jinja2 global variables
    app.jinja_env.globals.update(zip=jinja2_zip)
    
    return app  # Returning the Flask app instance

