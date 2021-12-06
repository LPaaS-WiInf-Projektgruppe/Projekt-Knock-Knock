from flask import Flask, render_template, Blueprint, request, redirect
from Models import ComOffers
from extensions import db
from datetime import datetime

comOffer = Blueprint('comOffer', __name__)


@comOffer.route('/comOffer', methods=['POST', 'GET'])
def createComOffer():
    if request.method == 'POST':
        content_start = request.form['start']
        content_ende = request.form['ende']
        content_zeit = request.form['zeit']
        content_geld = request.form['geld']
        content_dauer = request.form['dauer']
        zeitAlsPythonObjekt = datetime.strptime(content_zeit, '%Y-%m-%dT%H:%M')
        comoffer = ComOffers(
            start = content_start,
            destination = content_ende,
            kilometerpreis = content_geld,
            duration = content_dauer
        )
        # try:
        db.session.add(comoffer)
        db.session.commit()
        return redirect('/comOffer')
        # except:
        #     return 'An Error occured, while trying to add your offer :('
    else:
        allComOffers = ComOffers.query.order_by(ComOffers.id).all()
        return render_template('comOffer.html', view_name ='Company Offer', allComOffers=allComOffers)

@comOffer.route('/deleteComOffer/<int:id>')
def delete(id):
    comOffer_to_delete = comOffers.query.get_or_404(id)
    try:
        db.session.delete(comOffer_to_delete)
        db.session.commit()
        return redirect('/comOffer')
    except:
        return 'The offer could not be deleted :('
