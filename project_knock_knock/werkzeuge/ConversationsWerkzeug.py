from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect
from Models import ExchangedMessages, User
from extensions import db


conversations = Blueprint('conversations', __name__)


@conversations.route('/conversations', methods=['POST', 'GET'])
@login_required
def conversations_func():
    user = current_user
    conversations = User.get_conversations(user)
    return render_template('conversations.html', view_name ='Conversations', information=conversations)
