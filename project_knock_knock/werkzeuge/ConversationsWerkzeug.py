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

    dude = User.query.filter_by(id = conversations[0].get_id()).first()

    # print(f"conversations: {conversations[0].get_id()}")
    messages = ExchangedMessages.get_messages_for_user(user, dude)

    dude = User.query.filter(user.id == conversations[0].get_id()).first()

    return render_template(
        'conversations.html',
        information = conversations,
        dude = dude,
        self = user,
        messages = messages
    )
