from flask import Flask, render_template, Blueprint, request, redirect, url_for, jsonify
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
def com_offer():
    '''Show all available ComOffers
    '''

    create_com_offer_form = ComOfferForm()

    com_offers = ComOffers.get_available_offers()

    return render_template(
        'comOffer.html',
        view_name ='Company Offer',
        form=create_com_offer_form,
        offers = com_offers,
    )

@comOffer.route('/com_offer_detail/<int:offer_id>')
@login_required
def com_offer_detail_func(offer_id):
    com_offer = ComOffers.get_offer(offer_id)

    return render_template(
        'com_offer_detail.html',
        view_name ='Details',
        com_offer = com_offer
        )

@comOffer.route('/deleteComOffer/<int:id>')
@login_required
def delete(id):
    '''Delete the comOffer specified in the url
    '''

    if ComOffers.delete_offer(id):
        return redirect('/profil')
    else:
        return "Could not delete the Offer!"

@comOffer.route('/accept_com_offer/<int:offer_id>')
@login_required
def accept_offer(offer_id):
    '''Accept the com offer specified by the id in the url by adding the id
    of the user who accepted the offer to the respective entry in the com offer
    "accepted_by" column
    '''

    if ComOffers.accept_offer(offer_id, current_user):
        return redirect('/comOffer')
    else:
        return "You cannot accept your own offers!"

@comOffer.route("/create_com_offer", methods=["GET", "POST"])
@login_required
def create_com_offer():
    '''Create a com offer with the values received from the form
    '''
    form = ComOfferForm()

    if form.validate_on_submit():

        if ComOffers.create_offer(form, current_user):
            print("Offer created successfully")
            return redirect('/comOffer')
        else:
            print("Could not create offer")
            return "Could not create Com Offer"

    return render_template(
        "create_com_offer.html",
        view_name = "Create ComOffer",
        form = form
    )

@comOffer.route("/com_offer_coordinates", methods= ["POST"])
@login_required
def get_com_offer_coordinates():
    coordinates = ComOffers.get_all_coordinates()
    return jsonify(coordinates)
