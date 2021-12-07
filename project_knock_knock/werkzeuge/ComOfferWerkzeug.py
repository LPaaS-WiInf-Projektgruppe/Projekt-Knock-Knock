from flask import Flask, render_template, Blueprint, request, redirect, url_for
from flask_user import current_user, login_required
from Models import ComOffers
from extensions import db
from datetime import datetime
from forms.comOffer_form import ComOfferForm


comOffer = Blueprint('comOffer', __name__)


@comOffer.route('/comOffer', methods=['POST', 'GET'])
@login_required
def createComOffer():

 #form = ComOfferForm()

    if request.method == 'POST':
        content_start = request.form['von']
        content_ende = request.form['nach']
        content_start_zeit = request.form['input_start_date']
        content_end_zeit = request.form['input_end_date']
        content_geld = request.form['geld']

        startZeitAlsPythonObjekt = datetime.strptime(content_start_zeit, '%Y-%m-%dT%H:%M')


        if content_end_zeit == "":
            com_offer = ComOffers(
                start = content_start,
                destination = content_ende,
                start_time = startZeitAlsPythonObjekt,
                kilometerpreis = content_geld,
            )
        else:
            endZeitAlsPythonObjekt = datetime.strptime(content_end_zeit, '%Y-%m-%dT%H:%M')
            com_offer = ComOffers(
                start = content_start,
                destination = content_ende,
                start_time = startZeitAlsPythonObjekt,
                end_time = endZeitAlsPythonObjekt,
                kilometerpreis = content_geld,
            )


        try:
            db.session.add(com_offer)
            # associate a com_offer with a specific user
            com_offer.creator.append(current_user)
            db.session.commit()
            return redirect('/comOffer')
        except:
            return 'An Error occured, while trying to add your offer :('
    else:
        allComOffers = ComOffers.query.order_by(ComOffers.id).all()
        return render_template('comOffer.html', view_name ='Company Offer', allComOffers=allComOffers)

@comOffer.route('/deleteComOffer/<int:id>')
@login_required
def delete(id):
    comOffer_to_delete = ComOffers.query.get_or_404(id)
    try:
        db.session.delete(comOffer_to_delete)
        db.session.commit()
        return redirect('/comOffer')
    except:
        return 'The offer could not be deleted :('
