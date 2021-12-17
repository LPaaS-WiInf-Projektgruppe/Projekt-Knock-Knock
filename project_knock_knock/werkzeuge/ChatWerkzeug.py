from flask_user import login_required
from flask import Flask, render_template, Blueprint

chat = Blueprint('chat', __name__)


@chat.route('/chat')
# @login_required
def chat_func():

    return render_template(
        "chat.html",
        view_name='Chat',
        )
