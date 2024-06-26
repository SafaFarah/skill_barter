#!/usr/bin/python3

# app/routes.py

from flask import render_template, request, redirect, url_for
from app import app, db
from models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile_picture = request.form.get('profile_picture')  # Optional field

        # Create a new user instance
        new_user = User(username=username, email=email, password=password, profile_picture=profile_picture)

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
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Login Successful', 'success')
            return redirect(url_for('index'))  # Redirect to the home page after successful login
        else:
            flash('Invalid username or password', 'error')

    return render_template('signin.html')
