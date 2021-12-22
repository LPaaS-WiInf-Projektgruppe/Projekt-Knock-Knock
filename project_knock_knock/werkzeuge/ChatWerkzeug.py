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


        # Setzen des Status der Nachrichten auf gelesen, da sie im Anschluss geöffnet werden
        # Try Block, da nicht immer schon welche vorhanden
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


        return render_template("chat.html", view_name='Chat', dude = dude, self = self, messages = messages)


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
