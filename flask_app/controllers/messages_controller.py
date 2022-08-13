from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.register_model import Account
from flask_app.models.message_model import Message

@app.route('/send_message', methods=['POST'])
def send_message(): 
    data = {
        "sender_id": session['id'],
        "receiver_id": request.form['receiver_id'],
        "content": request.form['content'],
    }
    Message.save(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    Message.delete_message(data)
    return redirect('/dashboard')