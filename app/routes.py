from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models.user import User
from models.barter import Barter
from models.request import Request

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
        return render_template('main.html', user=user, user_id=user_id)
    flash('Please log in to access this page.', 'error')
    return redirect(url_for('signin'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))

    return render_template('profile.html', user=user, user_id=user_id)

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
        user.email = request.form.get('email')
        user.bio = request.form.get('bio')
        user.gender = request.form.get('gender')
        user.age = request.form.get('age')
        user.skills_i_have = ','.join(request.form.getlist('skills_i_have'))
        user.skills_i_want = ','.join(request.form.getlist('skills_i_want'))

        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile', user_id=user_id))

    # List of available skills
    skills = ['Python', 'C', 'C++', 'JavaScript', 'HTML', 'CSS', 'Data Analysis', 'Machine Learning']

    # Split user's skills into lists
    user_skills_i_have = user.skills_i_have.split(',') if user.skills_i_have else []
    user_skills_i_want = user.skills_i_want.split(',') if user.skills_i_want else []

    return render_template('edit_profile.html', user=user, user_id=user_id, skills=skills, user_skills_i_have=user_skills_i_have, user_skills_i_want=user_skills_i_want)

@app.route('/barter')
def barter():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page', 'error')
        return redirect(url_for('signin'))

    skill_offered = request.args.get('skill_offered', '')
    skill_requested = request.args.get('skill_requested', '')

    # Perform filtering based on skill_offered and skill_requested
    if skill_offered and skill_requested:
        barters = Barter.query.filter_by(skill_offered=skill_offered, skill_requested=skill_requested).all()
    elif skill_offered:
        barters = Barter.query.filter_by(skill_offered=skill_offered).all()
    elif skill_requested:
        barters = Barter.query.filter_by(skill_requested=skill_requested).all()
    else:
        barters = Barter.query.filter(Barter.status.in_(['available', 'requested'])).all()

    return render_template('barter.html', barters=barters, user_id=user_id)

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

        if not title or not skill_offered or not skill_requested:
            flash('Title, offered skill, and requested skill cannot be empty', 'error')
            return redirect(url_for('create_barter'))

        barter = Barter(
            title=title,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            description=description,
            user_id=user_id,
            status='available'
        )

        db.session.add(barter)
        db.session.commit()
        flash('Barter created successfully', 'success')
        return redirect(url_for('barter'))

    return render_template('create_barter.html', user=user, user_id=user_id)

@app.route('/barter_details/<int:barter_id>', methods=['GET', 'POST'])
def barter_details(barter_id):
    user_id = session.get('user_id')
    barter = Barter.query.get(barter_id)

    if not barter:
        flash('Barter not found', 'error')
        return redirect(url_for('main'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'request':
            # Handle request creation
            new_request = Request(
                user_id=user_id,
                barter_id=barter.id
            )
            db.session.add(new_request)
            db.session.commit()
            flash('Request sent successfully', 'success')

            # Update barter status to 'requested'
            barter.status = 'requested'
            barter.requester_id = user_id
            db.session.commit()
            return redirect(url_for('requests'))

        elif action == 'accept':
            # Handle request acceptance
            barter.status = 'accepted'
            db.session.commit()
            flash('Barter accepted successfully', 'success')
            return redirect(url_for('requests'))

        elif action == 'remove':
            # Handle request removal
            barter.status = 'available'
            barter.requester_id = None
            db.session.commit()
            flash('Request removed successfully', 'success')
            return redirect(url_for('requests'))

    return render_template('barter_details.html', barter=barter, user_id=user_id)

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
    requested_barters = Barter.query.filter_by(requester_id=user.id).filter(Barter.status != 'accepted').all()
    ongoing_barters = Barter.query.filter(
        (Barter.user_id == user_id) | (Barter.requester_id == user_id),
        Barter.status == 'accepted'
    ).all()

    return render_template('requests.html', user=user, user_id=user_id, my_barters=my_barters, requested_barters=requested_barters, ongoing_barters=ongoing_barters)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
