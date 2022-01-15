from flask import Flask, render_template, Blueprint, request, redirect, jsonify, make_response
from flask_user import current_user, login_required
from Models import DriverOffers, WorkingTime, User
from extensions import db
from datetime import datetime, timedelta

from forms.driverOffer_form import DriverOfferForm
from forms.search_drive_offer_form import SearchDriveOfferForm
from config import API_KEY

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
@login_required
def driver_offer():
    form = SearchDriveOfferForm()

    if form.validate_on_submit():
        driver_offers = DriverOffers.search_offer_by_location(
            form.von.data,
            form.nach.data
        )

        return render_template(
            'driverOffer.html',
            view_name ='Drive Offer',
            allDriverOffers=driver_offers,
            form = form,
            api_key = API_KEY
            )
    allDriverOffers = DriverOffers.get_offers()

    driver_offers = []

    # print(allDriverOffers)

    return render_template(
        'search_drive_offer.html',
        view_name ='Driver Offer',
        allDriverOffers=driver_offers,
        form = form,
        api_key = API_KEY
        )

@driverOffer.route('/drive_offer_detail/<int:offer_id>')
@login_required
def driver_offer_detail_func(offer_id):

    driver_offers = DriverOffers.get_offer(offer_id)

    return render_template(
        'driver_offer_detail.html',
        view_name ='Details',
        drive_offer = driver_offers
        )

@driverOffer.route('/delete_driver_offer/<int:id>')
def delete(id):
    '''Delete the drive offer specified by the id in the url
    :param id int: the id of the drive offer to delete
    '''

    if DriverOffers.delete_offer(id):
        return redirect("/profil")

    else:
        return 'The offer could not be deleted :('

@driverOffer.route('/accept_drive_offer/<int:offer_id>')
def accept_offer(offer_id):
    '''Accept the drive offer specified by the id in the url by adding the id
    of the user who accepted the offer to the respective entry in the drive offer
    "accepted_by" column
    :param offer_id int: The ID of the offer to accept
    '''

    if DriverOffers.accept_offer(offer_id, current_user):
        return redirect('/driverOffer')
    else:
        return "Offer Could not be accepted :("

@driverOffer.route("/create_drive_offer", methods=["GET", "POST"])
@login_required
def create_drive_offer():
    '''Creates a new DriveOffer
    '''
    form = DriverOfferForm()

    if form.validate_on_submit():
        if DriverOffers.create_offer(form, current_user):
            return redirect("/driverOffer")
        else:
            return 'An Error occured, while trying to add your offer :('

    return render_template(
        "create_drive_offer.html",
        view_name = "Create Driver Offer",
        form = form
    )

@driverOffer.route("/geocode_location/<string:location>", methods=["POST"])
def geocode_location(location):
    '''Convert a List of locations to their respective
    Latitude and Longitude Coordinates
    '''

    print(location)
    coord = DriverOffers.geocode_location([location])[0]


    return jsonify({"latitude": coord.latitude, "longitude": coord.longitude})
