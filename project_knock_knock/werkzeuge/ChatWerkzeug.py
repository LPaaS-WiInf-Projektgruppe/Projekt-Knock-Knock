from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect, url_for, session
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

    dude = User.query.filter_by(id = dude_id).first()
    self = current_user

    if request.method == 'POST' :
        content_text = request.form['send']
        new_message = ExchangedMessages(transmitter = self.id, receiver = dude.id, text = content_text, read = False)
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect("/chat/" + str(dude.id))
        except:
            return 'Nachricht konnte nicht versendet werden :/'

    else:
        #messages = ExchangedMessages.query.order_by(ExchangedMessages.created_at).filter(and_(
        #            or_(ExchangedMessages.transmitter == dude.id),
        #            or_(ExchangedMessages.transmitter == self.id),
        #            or_(ExchangedMessages.receiver == dude.id),
        #            or_(ExchangedMessages.receiver == self.id))
        #            ).all()


        messages = ExchangedMessages.query.order_by(ExchangedMessages.created_at).filter(and_(
                    or_(ExchangedMessages.transmitter == dude.id, ExchangedMessages.transmitter == self.id),
                    or_(ExchangedMessages.receiver == dude.id, ExchangedMessages.receiver == self.id))
                    ).all()



        return render_template("chat.html", view_name='Chat', dude = dude, self = self, messages = messages)
