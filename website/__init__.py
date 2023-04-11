# Importing necessary modules and Libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import create_engine
from flask_migrate import Migrate
from builtins import zip


password='test%401234'
admin_name = 'milton'
uri = f'postgresql+psycopg2://{admin_name}:{password}@elp-server.postgres.database.azure.com/postgres?sslmode=require'
db = SQLAlchemy()

# Function to create Flask app instance
def create_app():
    app = Flask(__name__) # Creating Flask app instance
    # Setting configuration parameters
    app.config.from_mapping(
        SECRET_KEY='mrcaptain@12345.vectorized.ithinkthisisverystrongforasecuritykey',  # A secret key for securely signing session cookies and other security-related needs
        SQLALCHEMY_DATABASE_URI=uri, # The URI for accessing the PostgreSQL database
        SQLALCHEMY_TRACK_MODIFICATIONS=True  # Enables tracking modifications for SQLAlchemy, could be set to False incase of perfomance issues
    )
    

    db.init_app(app)  # Initialize SQLAlchemy with the Flask app

    # Importing views and auth blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views) # Registering the views blueprint
    app.register_blueprint(auth, url_prefix='/auth')# Registering the auth blueprint with a prefix URL

    from .models import User

    with app.app_context():
        # Creating all tables in the database using the defined models. Use db.drop_all() to drop all tables
        db.create_all()  

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

