from flask import Blueprint, render_template, url_for, request, flash, jsonify, redirect
from flask_login import login_required,  current_user
from flask_wtf.csrf import generate_csrf
from .models import User, Note,AlumniScholarProfiles, Events, Careers
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'] )
def home():
    # if request.method == 'POST':
    #     note = request.form.get('note')
        
    #     if len(note) < 1:
    #         flash('Note is too short', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash("Note added!", category='success') 
    return render_template("home.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)



@views.route('/events', methods=['GET', 'POST'])
def events():
    events = Events.query.order_by(Events.event_date.asc()).all()
    return render_template("events.html", user=current_user, events=events)

@views.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        event = Events(
            user_id=current_user.id,
            event_name=request.form.get('event_name'),
            event_venue=request.form.get('event_venue'),
            event_date=datetime.strptime(request.form.get('event_date'), '%Y-%m-%dT%H:%M') if request.form.get('event_date') else None,
            event_description=request.form.get('event_description'),
            phone_number=request.form.get('phone_number'),
            email=request.form.get('email')
        )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('views.events'))
    csrf_token = generate_csrf()
    return render_template("create_event.html", user=current_user, csrf_token=csrf_token)


@views.route('/careers')
def careers():
    careers = Careers.query.order_by(Careers.date_published.asc()).all()
    
    return render_template("careers.html", user=current_user, careers=careers)

@views.route('/create-job-listing', methods=['GET', 'POST'])
def create_job_listing():
    if request.method == 'POST':
        career = Careers(
            user_id=current_user.id,
            job_title=request.form.get('job_title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            salary=request.form.get('salary'),
            deadline_date=request.form.get('dealine_date'),
            job_description=request.form.get('job_description'),
            phone_number=request.form.get('phone_number'),
            email=request.form.get('email')
        )
        db.session.add(career)
        db.session.commit()
        flash('Your job listing has been created!', 'success')
        return redirect(url_for('views.careers'))
    return render_template("create_job.html", user=current_user)


@views.route('/find-alumni', methods=['GET', 'POST'])
def find_alumni():
    scholars = User.query.order_by(User.firstname.asc()).all()
    # scholar_profiles = [scholar.profile for scholar in scholars]
    return render_template("find_alumni.html", user=current_user, scholars=scholars)


@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
   
    return jsonify({})