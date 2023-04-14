from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, AlumniScholarProfiles, Events, Careers
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def dashboard():
    user_count = User.query.count()
    event_count = Events.query.count()
    career_count = Careers.query.count()
    return render_template('admin/dashboard.html', user=current_user, user_count=user_count, event_count=event_count, career_count=career_count)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

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
    return render_template("admin/login.html", user=current_user)

@admin.route('/users')
@login_required
def users():
    scholars = User.query.all()
    return render_template('admin/users.html', user=current_user, scholars=scholars)

@admin.route('/events')
@login_required
def events():
    events = Events.query.all()
    return render_template('admin/admin_event.html',user=current_user, events=events)

@admin.route('/careers')
@login_required
def careers():
    careers = Careers.query.all()
    return render_template('admin/job_posts.html',user=current_user, careers=careers)


@admin.route('/admin/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Events.query.get(event_id)
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('admin.events'))
    if request.method == 'POST':
        event.event_name = request.form['event_name']
        event.event_venue = request.form['event_venue']
        event.event_date = request.form['event_date']
        event.event_description = request.form['event_description']
        event.phone_number = request.form['phone_number']
        event.email = request.form['email']
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/edit_event.html',user=current_user, event=event)

@admin.route('/admin/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Events.query.get(event_id)
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('admin.events'))
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin.events'))


@admin.route('/career/edit/<int:career_id>', methods=['GET', 'POST'])
@login_required
def edit_career(career_id):
    career = Careers.query.get(career_id)
    if request.method == 'POST':
        career.job_title = request.form.get('job_title')
        career.company = request.form.get('company')
        career.location = request.form.get('location')
        career.salary = request.form.get('salary')
        career.deadline_date = request.form.get('deadline_date')
        career.job_description = request.form.get('job_description')
        career.phone_number = request.form.get('phone_number')
        career.email = request.form.get('email')
        db.session.commit()
        flash('Career updated successfully!', 'success')
        return redirect(url_for('careers'))
    return render_template('admin/edit_job.html', user=current_user,career=career)


@admin.route('/career/delete/<int:career_id>', methods=['GET', 'POST'])
@login_required
def delete_career(career_id):
    career = Careers.query.get(career_id)
    if not career:
        flash('Job not found!', 'error')
    db.session.delete(career)
    db.session.commit()
    flash('Career deleted successfully!', 'success')
    return redirect(url_for('admin.careers'))
