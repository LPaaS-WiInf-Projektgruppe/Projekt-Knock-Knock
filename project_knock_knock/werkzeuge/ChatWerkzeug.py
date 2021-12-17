from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect
from Models import ExchangedMessages, User
from extensions import db

chat = Blueprint('chat', __name__)


@chat.route('/chat')
@login_required
def chat_test():

    return render_template("chat.html", view_name='Chat',)



@chat.route('/chat/<int:dude_id>')
@login_required
def chat_func(dude_id):
    result = User.query.filter_by(id = dude_id).first()
    return render_template("chat.html", view_name='Chat',dude = result)
