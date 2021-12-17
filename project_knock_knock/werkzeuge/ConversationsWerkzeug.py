from flask_user import login_required
from flask import Flask, render_template, Blueprint

conversations = Blueprint('conversations', __name__)


@conversations.route('/conversations')
# @login_required
def conversations_func():

    return render_template(
        "conversations.html",
        view_name='Conversations',
        )
