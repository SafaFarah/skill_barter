from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models.user import User
from models.barter import Barter
from werkzeug.utils import secure_filename
import os
from PIL import Image

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('index.html', user=user)
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            return redirect(url_for('signup'))

        # Create a new user instance
        new_user = User(username=username, email=email, password=password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Signup Successful', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('Login Successful', 'success')
            session['user_id'] = user.id
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('signin.html')

@app.route('/main')
def main():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('main.html', user=user)
    flash('Please log in to access this page.', 'error')
    return redirect(url_for('signin'))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    return render_template('profile.html', user=user)

# Set the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash('Username cannot be empty', 'error')
            return redirect(url_for('edit_profile'))

        user.username = username
        user.username = username
        user.email = request.form.get('email')
        user.bio = request.form.get('bio')
        user.gender = request.form.get('gender')
        user.age = request.form.get('age')
        user.skills_i_have = ','.join(request.form.getlist('skills_i_have'))
        user.skills_i_want = ','.join(request.form.getlist('skills_i_want'))
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))

    skills = ['Python', 'JavaScript', 'HTML', 'CSS', 'Data Analysis', 'Machine Learning']  # Add more skills as needed
    user_skills_i_have = user.skills_i_have.split(',') if user.skills_i_have else []
    user_skills_i_want = user.skills_i_want.split(',') if user.skills_i_want else []

    return render_template('edit_profile.html', user=user, skills=skills, user_skills_i_have=user_skills_i_have, user_skills_i_want=user_skills_i_want)

@app.route('/barter')
def barter():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view this page', 'error')
        return redirect(url_for('signin'))

    barters = Barter.query.filter_by(user_id=user_id).all()
    return render_template('barter.html', barters=barters)


@app.route('/create_barter', methods=['GET', 'POST'])
def create_barter():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        title = request.form.get('title')
        skill_offered = request.form.get('skill_offered')
        skill_requested = request.form.get('skill_requested')
        description = request.form.get('description')

        # Create a new barter object
        new_barter = Barter(
            title=title,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            description=description,
            user_id=user.id  # Assign the logged-in user's ID to the barter
        )

        db.session.add(new_barter)
        db.session.commit()

        flash('Barter created successfully', 'success')
        return redirect(url_for('requests'))  # Redirect to requests page after creating barter

    return render_template('create_barter.html', user=user)


@app.route('/requests')
def requests():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    # Fetch barters created by the logged-in user
    my_barters = Barter.query.filter_by(user_id=user.id).all()

    # Fetch barters requested by the logged-in user
    requested_barters = Barter.query.filter_by(requester_id=user.id).all()

    # You may have another method to fetch responses to the user's barters
    barter_responses = []  # Replace with your logic to fetch responses

    return render_template('requests.html', user=user, my_barters=my_barters, requested_barters=requested_barters, barter_responses=barter_responses)

@app.route('/ongoing_barters')
def ongoing_barters():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    # Query barters where both parties have accepted (assuming a 'accepted' status)
    ongoing_barters = Barter.query.filter_by(status='accepted').all()

    return render_template('ongoing_barters.html', user=user, ongoing_barters=ongoing_barters)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
