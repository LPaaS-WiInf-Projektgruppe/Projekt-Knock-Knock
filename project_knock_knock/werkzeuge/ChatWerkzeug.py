from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, jsonify
from Models import ExchangedMessages, User
from extensions import db
from sqlalchemy import or_, and_

chat = Blueprint('chat', __name__)


@chat.route('/chat')
@login_required
def chat_test():

    return render_template("chat.html", view_name='Chat',)

@chat.route('/chat/<int:dude_id>', methods=['POST', 'GET'])
@login_required
def chat_func(dude_id):

    user = current_user
    messages = ExchangedMessages.get_messages_for_user(user, dude_id)

    return render_template("chat.html", view_name='Chat', dude = dude, self = user, messages = messages)


@chat.route('/update_chat/<int:dude_id>', methods=['POST'])
@login_required
def update(dude_id):

    dude = User.query.filter_by(id = dude_id).first()
    self = current_user

    try:
        message = ExchangedMessages.query.order_by(ExchangedMessages.created_at.desc()).filter(
                    and_(ExchangedMessages.transmitter == dude.id, ExchangedMessages.receiver == self.id)
                    ).first()
        gelesen = ExchangedMessages.query.filter(ExchangedMessages.id == message.id).first().read

        if gelesen == False:
            ExchangedMessages.query.filter(ExchangedMessages.id == message.id).update({"read": True})
            db.session.commit()
    except:
        pass

    # Übergabe der Nachrichten aus dem ausgewählten Chat
    messages = ExchangedMessages.query.order_by(ExchangedMessages.created_at).filter(or_(
            and_(ExchangedMessages.transmitter == dude.id, ExchangedMessages.receiver == self.id),
            and_(ExchangedMessages.transmitter == self.id, ExchangedMessages.receiver == dude.id)
                )).all()

    return jsonify('', render_template('chat_refresh.html', view_name='Chat', dude = dude, self = self, messages = messages))
    #return render_template("chat.html", view_name='Chat', dude = dude, self = self, messages = messages)
