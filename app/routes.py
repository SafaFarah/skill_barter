from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models.user import User
from models.barter import Barter  # Assuming you have a Barter model

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
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('signin.html')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    return render_template('profile.html', user=user)

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.profile_picture = request.form.get('profile_picture')

        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))

    return render_template('edit-profile.html', user=user)

@app.route('/barter', methods=['GET', 'POST'])
def barter():
    if request.method == 'POST':
        skill_offered = request.form['skill_offered']
        skill_requested = request.form['skill_requested']
        user_id = session.get('user_id')

        new_barter = Barter(skill_offered=skill_offered, skill_requested=skill_requested, user_id=user_id)
        db.session.add(new_barter)
        db.session.commit()

        flash('Barter Created Successfully', 'success')
        return redirect(url_for('index'))

    return render_template('barter.html')

@app.route('/requests')
def requests():
    return render_template('requests.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))