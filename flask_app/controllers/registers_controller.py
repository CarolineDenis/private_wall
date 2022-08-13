from crypt import methods
from email import message
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.message_model import Message
from flask_app.models.register_model import Account
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "email" in session:
    # can have access to dashboard by URL if still email in session 
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    if not Account.validate_form(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    new_user = Account.save(data)
    session['id'] = new_user
    session['email'] = request.form['email']
    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    data = {
        'email': request.form['email'],
    }
    user_in_db = Account.get_by_email(data)
    if not user_in_db:
        flash("Invalid Password/Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Password")
            return redirect('/')
    if user_in_db:
        session['email'] = user_in_db.email
        session['id'] = user_in_db.id
        return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if not "email" in session:
        return redirect('/')
    data = {
        'email': session['email'],
        'id': session['id']
    }
    users = Account.get_all()
    user = Account.get_by_email(data)
    messages = Message.get_all_for_user(data)
    sent_messages = Message.get_all_sent(data)
    return render_template("user_page.html", users=users, user=user, messages=messages, sent_messages=sent_messages)

@app.route("/delete_session")
def delete_session():
    session.clear()
    return redirect("/")