from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, AlumniScholarProfiles, Events, Careers
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

admin = Blueprint('admin', __name__)

# Login route
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  
         
        # Check if user exists in the database
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
