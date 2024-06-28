# app/routes.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models.user import User

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('index.html', user_id=user_id, user=user)
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
        # Optionally, you can redirect to a login page or any other page after successful signup
        return redirect(url_for('signin'))
    # Render the signup form template for GET requests
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Simplified example, use proper password hashing in production
            flash('Login Successful', 'success')
            session['user_id'] = str(user.ID)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    # Render the signin form template for GET requests
    return render_template('signin.html')

@app.route('/profile/<string:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        return 'User not found', 404

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if request.method == 'POST':
        # Update user profile
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.profile_picture = request.form.get('profile_picture')

        # Commit changes to the database
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile', user_id=user.ID))

    # Render the edit profile form with current user information for GET requests
    return render_template('edit-profile.html', user=user)

@app.route('/requests')
def requests():
    return render_template('requests.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/barter', methods=['GET', 'POST'])
def barter():
    if request.method == 'POST':
        skill_offered = request.form['skill_offered']
        skill_requested = request.form['skill_requested']
        user_id = session.get('user_id')  # Assuming you store user_id in session after login

        # Create a new barter instance
        new_barter = Barter(skill_offered=skill_offered, skill_requested=skill_requested, user_id=user_id)

        # Add the barter to the database
        db.session.add(new_barter)
        db.session.commit()

        flash('Barter Created Successfully', 'success')

        # Redirect to another page after creating the barter
        return redirect(url_for('index'))

    # Render the barter creation form template for GET requests
    return render_template('Barter.html')
