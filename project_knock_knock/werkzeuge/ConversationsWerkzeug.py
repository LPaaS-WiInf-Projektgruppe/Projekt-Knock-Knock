from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect
from Models import ExchangedMessages, User
from extensions import db

conversations = Blueprint('conversations', __name__)


@conversations.route('/conversations', methods=['POST', 'GET'])
@login_required
def conversations_func():

    #zu Testzwecken noch auskommentiert
    #allContacts = ExchangedMessages.query.order_by(ExchangedMessages.created_at).all()
    allContacts = User.query.order_by(User.id).all()

    return render_template('conversations.html', view_name ='Conversations', allContacts=allContacts)
