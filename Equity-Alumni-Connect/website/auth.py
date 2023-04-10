from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, AlumniScholarProfiles
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')   
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else: 
            flash('Account does not exist. Create a new account', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        print(user)
        
        if user:
            flash('Email already exists', category='error')     
        
        elif len(email) < 4:
            flash('Invalid email!', category='error') 
        elif len(firstname) < 2:
            flash('Name must be more than 2 characters!', category='error') 
        elif len(lastname) < 2:
            flash('Name must be more than 2 characters!', category='error') 
        elif password != password2:
            flash('Passwords do not match!', category='error') 
        else: 
            new_user = User(
                email=email, 
                firstname=firstname,
                lastname=lastname,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True, force=True) 
            flash('Account created successfully!',category='success')
            
            return redirect(url_for('auth.create_profile')) 
    
    return render_template("signup.html", user=current_user)

@auth.route('/create-profile', methods=['GET', 'POST'])
@login_required
def create_profile():  
    if request.method  == 'POST':
        scholars_code = request.form.get('scholarsCode')
        primary_number = request.form.get('primaryNumber')
        secondary_number = request.form.get('secondaryNumber')
        country = request.form.get('country')
        home_county = request.form.get('homeCounty')
        current_county = request.form.get('currentCounty')
        equity_home_branch = request.form.get('Equity-home-branch')
        school_university_college = request.form.get('schoolUniversity')
        course = request.form.get('course')
        interests = request.form.get('interests')
        hobbies = request.form.get('hobbies') 
        
        new_profile = AlumniScholarProfiles (
            user_id = current_user.id,
            scholars_code=scholars_code,
            primary_number=primary_number,
            secondary_number=secondary_number,
            country=country,
            home_county=home_county,
            current_county=current_county,
            equity_home_branch=equity_home_branch,
            school_university_college=school_university_college,
            course=course,
            interests=interests,
            hobbies=hobbies      
        )
        db.session.add(new_profile)
        db.session.commit()    
        flash('Profile created successfully!',category='success') 
        return redirect(url_for('views.home'))
               
    return render_template('create_profile.html', user=current_user)

