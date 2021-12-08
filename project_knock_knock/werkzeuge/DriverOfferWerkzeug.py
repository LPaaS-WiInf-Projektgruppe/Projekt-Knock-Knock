from flask import Flask, render_template, Blueprint, request, redirect, url_for
from flask_user import current_user, login_required
from Models import DriverOffers
from extensions import db
from datetime import datetime, timedelta
from forms.driverOffer_form import DriverOfferForm
import re

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
@login_required
def createDriverOffer():

    form = DriverOfferForm()

    # if request.method == 'POST':

    if form.validate_on_submit():
        content_ort = request.form['ort']
        content_fahrzeug = request.form['fahrzeug']
        content_verfügbarVon = request.form['verfügbarVon']
        content_verfügbarBis = request.form['verfügbarBis']
        content_zeitMo = request.form['zeitMo']
        content_zeitDi = request.form['zeitDi']
        content_zeitMi = request.form['zeitMi']
        content_zeitDo = request.form['zeitDo']
        content_zeitFr = request.form['zeitFr']
        content_zeitSa = request.form['zeitSa']
        content_zeitSo = request.form['zeitSo']
        content_preis = request.form['preis']
        content_umkreis = request.form['umkreis']
        content_bemerkungen = request.form['bemerkungen']

        #formatted_datetime = content_start_zeit[:8] + '-' + content_start_zeit[9:]

        verfügbarVonAlsPythonObjekt = datetime.strptime(content_verfügbarVon, '%d.%m.%Y-%H:%M')
        verfügbarBisAlsPythonObjekt = datetime.strptime(content_verfügbarBis, '%d.%m.%Y-%H:%M')

        driver_offer = DriverOffers(
        location = content_ort,
        vehicle = content_fahrzeug,
        start_time = verfügbarVonAlsPythonObjekt,
        end_time = verfügbarVonAlsPythonObjekt,
        #zeitMo = content_zeitMo,
        #zeitDi = content_zeitDi,
        #zeitMi = content_zeitMi,
        #zeitDo = content_zeitDo,
        #zeitFr = content_zeitFr,
        #zeitSa = content_zeitSa,
        #zeitSo = content_zeitSo,
        kilometerpreis = content_preis,
        radius = content_umkreis,
        text = content_bemerkungen,
        )

        try:
            db.session.add(driver_offer)
            # associate a driver_offer with a specific user
            #driver_offer.creator.append(current_user)
            db.session.commit()
            return redirect('/driverOffer')
        except:
            return 'An Error occured, while trying to add your offer :('
    else:
        allDriverOffers = DriverOffers.query.order_by(DriverOffers.id).all()
        return render_template(
            'driverOffer.html',
            view_name ='Driver Offer',
            allDriverOffers = allDriverOffers,
            form = form
        )



@driverOffer.route('/deleteDriverOffer/<int:id>')
def delete(id):
    driverOffer_to_delete = DriverOffers.query.get_or_404(id)
    try:
        db.session.delete(driverOffer_to_delete)
        db.session.commit()
        return redirect('/driverOffer')
    except:
        return 'The offer could not be deleted :('
