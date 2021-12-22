from flask import Flask, render_template, Blueprint, request, redirect, url_for
from flask_user import current_user, login_required
from Models import ComOffers, User
from extensions import db
from datetime import datetime
from forms.comOffer_form import ComOfferForm
from materialien.com_offer import ComOffer
import re


comOffer = Blueprint('comOffer', __name__)


@comOffer.route('/comOffer', methods=['POST', 'GET'])
@login_required
def createComOffer():
    allComOffers = ComOffers.query.order_by(ComOffers.id).all()

    com_offers = []
    for offer in allComOffers:
        # format_start_time = datetime.strptime(offer.start_time,"%YYYY-mm-dd hh:mm:ss")
        # format_end_time = datetime.strptime(offer.end_time,"%YYYY-mm-dd hh:mm:ss")
        format_start_time = offer.start_time.strftime("%d.%m.%y %H:%M")
        format_end_time = offer.end_time.strftime("%d.%m.%y %H:%M")
        com_offer = ComOffer(
            offer.id,
            offer.start,
            offer.destination,
            format_start_time,
            format_end_time,
            offer.kilometerpreis,
            offer.created_at,
            offer.creator,
            0
        )
        com_offers.append(com_offer)

    return render_template(
        'comOffer.html',
        view_name ='Company Offer',
        offers = com_offers,
    )

@comOffer.route('/deleteComOffer/<int:id>')
@login_required
def delete(id):
    '''delete the comOffer specified in the url'''
    comOffer_to_delete = ComOffers.query.get_or_404(id)
    try:
        if comOffer_to_delete.accepted_by == "NULL":
            db.session.delete(comOffer_to_delete)
            db.session.commit()
            return redirect('/comOffer')
        else:
            return "You cannot delete an offer that has already been accepted!"
    except:
        return 'The offer could not be deleted :('


@comOffer.route('/accept_com_offer/<int:offer_id>')
def accept_offer(offer_id):
    ''' accept the com offer specified by the id in the url by adding the id
    of the user who accepted the offer to the respective entry in the com offer
    "accepted_by" column
    '''

    # query database for every drive offer that the user accepted
    user, com_offer = db.session.query(User, ComOffers) \
        .join(User, ComOffers.creator) \
        .filter(ComOffers.id == offer_id) \
        .first()


    if user.username != current_user.username:
        com_offer.accepted_by = current_user.id
        db.session.commit()
        return redirect('/comOffer')
    else:
        return "You cannot accept your own offers!"

@comOffer.route("/create_com_offer", methods=["GET", "POST"])
@login_required
def create_com_offer():

    form = ComOfferForm()

    if form.validate_on_submit():
        content_start = request.form['von']
        content_ende = request.form['nach']
        content_start_zeit = request.form['zeit_start']
        content_end_zeit = request.form['zeit_ende']
        content_geld = request.form['geld']

        formatted_start_zeit = content_start_zeit[:10] + '-' + content_start_zeit[11:]
        formatted_end_zeit = content_start_zeit[:10] + '-' + content_start_zeit[11:]

        startZeitAlsPythonObjekt = datetime.strptime(formatted_start_zeit, '%d.%m.%Y-%H:%M')


        if content_end_zeit == "":
            com_offer = ComOffers(
                start = content_start,
                destination = content_ende,
                start_time = startZeitAlsPythonObjekt,
                kilometerpreis = content_geld
            )
        else:
            endZeitAlsPythonObjekt = datetime.strptime(formatted_end_zeit, '%d.%m.%Y-%H:%M')
            com_offer = ComOffers(
                start = content_start,
                destination = content_ende,
                start_time = startZeitAlsPythonObjekt,
                end_time = endZeitAlsPythonObjekt,
                kilometerpreis = content_geld
            )


        try:
            db.session.add(com_offer)
            # associate a com_offer with a specific user
            com_offer.creator.append(current_user)
            db.session.commit()
            return redirect('/comOffer')
        except:
            return 'An Error occured, while trying to add your offer :('

    return render_template(
        "create_com_offer.html",
        view_name = "Create ComOffer",
        form = form
    )
