from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, request, redirect
from Models import ExchangedMessages, User
from extensions import db
from sqlalchemy import or_, and_


conversations = Blueprint('conversations', __name__)


@conversations.route('/conversations', methods=['POST', 'GET'])
@login_required
def conversations_func():

    #-----------gibt sicher einen eleganteren Weg sry--------------

    self = current_user

    # Ermittelt alle für den User relevanten Konversationen
    allParticipatedConversations = ExchangedMessages.query.order_by(ExchangedMessages.created_at.desc()).filter(
                                    or_(ExchangedMessages.transmitter == self.id, ExchangedMessages.receiver == self.id)
                                    ).all()

    # Sammelt alle disjunkten bisherigen Kommunikationspartner
    allContacts = []

    for conversation in allParticipatedConversations:
        if conversation.transmitter not in allContacts:
            allContacts.append(conversation.transmitter)
        if conversation.receiver not in allContacts:
            allContacts.append(conversation.receiver)

    # Mit dieser Klasse werden Objekte erstellt, damit Daten zusammenhängend
    # an die HTML-Seite weitergegeben werden können
    class InfoForHTML():
        def __init__(self, id, name, zeit, gelesen):
            self.id = id
            self.name = name
            self.zeit = zeit
            self.gelesen = gelesen

    # Sammlung der jeweiligen Objekte über die Kommunikationspartner
    toBeDisplayed = []

    # Erstellung der Objekte für die obige Sammlung
    for contact in allContacts:
        typ = User.query.filter_by(id = contact).first()
        try:
            zeit = ExchangedMessages.query.order_by(ExchangedMessages.created_at.desc()).filter(or_(
                    and_(ExchangedMessages.transmitter == self.id, ExchangedMessages.receiver == typ.id),
                    and_(ExchangedMessages.transmitter == typ.id, ExchangedMessages.receiver == self.id)
                    )).first().created_at
            gelesen = ExchangedMessages.query.order_by(ExchangedMessages.created_at.desc()).filter(
                        and_(ExchangedMessages.transmitter == typ.id, ExchangedMessages.receiver == self.id)
                        ).first().read
            infoRow  = InfoForHTML(typ.id, typ.username, zeit, gelesen)
            toBeDisplayed.append(infoRow)
        except:
            pass
            # Auskommentierter Kommentar zum  Debuging, except und pass müssen aber bleiben
            # für den Fall von (noch) nicht existierenden Konversationen
            #return "Eigener Username: " + self.username + " und Nummer: " +str(self.id) + "\n" + "Andererer Dude: " + typ.username + " und Nummer: " +str(typ.id) + "\n" + "Letzte ausgetauschte Nachricht: " + "\n" + str(allContacts)



    #-----------Ende vom üblen Teil hehe----------------


    return render_template('conversations.html', view_name ='Conversations', information=toBeDisplayed)
