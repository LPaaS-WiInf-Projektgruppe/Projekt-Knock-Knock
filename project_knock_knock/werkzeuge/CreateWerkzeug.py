from flask import Flask, render_template, Blueprint, request, redirect
from Models import comOffers
from extensions import db
from datetime import datetime

create = Blueprint('create', __name__)


@create.route('/create', methods=['POST', 'GET'])
def createComOffer():
    if request.method == 'POST':
        content_start = request.form['start']
        content_ende = request.form['ende']
        content_zeit = request.form['zeit']
        content_geld = request.form['geld']
        zeitAlsPythonObjekt = datetime.strptime(content_zeit, '%Y-%m-%dT%H:%M')
        new_ComOffer = comOffers(start = content_start, end = content_ende, time = zeitAlsPythonObjekt, money = content_geld)
        try:
            db.session.add(new_ComOffer)
            db.session.commit()
            return redirect('/create')
        except:
            #return 'An Error occured, while trying to add your offer :('
            return content_zeit
    else:
        allOffers = comOffers.query.order_by(comOffers.id).all()
        return render_template('create.html', view_name ='Create', allOffers=allOffers)

@create.route('/deleteComOffer/<int:id>')
def delete(id):
    offer_to_delete = comOffers.query.get_or_404(id)
    try:
        db.session.delete(offer_to_delete)
        db.session.commit()
        return redirect('/create')
    except:
        return 'The offer could not be deleted :('
