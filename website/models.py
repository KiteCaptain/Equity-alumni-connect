from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    notes = db.relationship('Note')
    user_profile = db.relationship('AlumniScholarProfiles', backref='user')
    event_created = db.relationship('Events', backref='user')
    job_created = db.relationship('Careers', backref='user')
    
    
class AlumniScholarProfiles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    scholars_code=db.Column(db.String(150))
    primary_number=db.Column(db.String(20))
    secondary_number=db.Column(db.String(20))    
    country=db.Column(db.String(150))
    home_county=db.Column(db.String(150))
    current_county=db.Column(db.String(150))
    equity_home_branch=db.Column(db.String(150))
    school_university_college=db.Column(db.String(150))
    course=db.Column(db.String(200))
    interests=db.Column(db.String(500))
    hobbies=db.Column(db.String(500))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    

class Events(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    event_poster=db.Column(db.LargeBinary(), nullable=True)
    event_name=db.Column(db.String(500))
    event_venue=db.Column(db.String(500))
    event_date=db.Column(db.DateTime(timezone=True))
    created_date=db.Column(db.DateTime(timezone=True), default=func.now())
    event_description=db.Column(db.String(2000))
    phone_number=db.Column(db.String(20))
    email=db.Column(db.String(150))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class Careers(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    job_title=db.Column(db.String(100))
    company=db.Column(db.String(100))
    location=db.Column(db.String(100))
    salary=db.Column(db.String(100))
    date_published=db.Column(db.DateTime(timezone=True), default=func.now())
    deadline_date=db.Column(db.DateTime(timezone=True))
    job_description=db.Column(db.String(2000))
    phone_number=db.Column(db.String(20))
    email=db.Column(db.String(150))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    

    