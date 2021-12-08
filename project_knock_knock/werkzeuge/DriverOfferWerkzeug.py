from flask import Flask, render_template, Blueprint, request, redirect, url_for
from flask_user import current_user, login_required
from Models import DriverOffers, WorkingTime
from extensions import db
from datetime import datetime, timedelta
from forms.driverOffer_form import DriverOfferForm
import re

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
@login_required
def createDriverOffer():

    form = DriverOfferForm()


    # add work time information from form to database and append it to current user
    i = 0
    for results in request.form:
        if (results == "from_zeitMo" or results == "from_zeitDi" or results == "from_zeitMi" or \
        results == "from_zeitDo" or results == "from_zeitFr" or results == "from_zeitSa" or \
        results == "from_zeitSo"):

            bis = datetime.strptime(request.form[results],'%H:%M')
            bis += timedelta(hours=8)
            bis.strftime("%H:%M")
            working_time = WorkingTime(
                weekday = i,
                start_time = request.form[results],
                end_time = bis
            )
            db.session.add(working_time)
            working_time.driver.append(current_user)
        i+=1


    if form.validate_on_submit():
        content_ort = request.form['ort']
        content_fahrzeug = request.form['fahrzeug']
        content_verfügbarVon = request.form['verfügbarVon']
        content_verfügbarBis = request.form['verfügbarBis']
        content_zeitMo = request.form['from_zeitMo']
        content_zeitDi = request.form['from_zeitDi']
        content_zeitMi = request.form['from_zeitMi']
        content_zeitDo = request.form['from_zeitDo']
        content_zeitFr = request.form['from_zeitFr']
        content_zeitSa = request.form['from_zeitSa']
        content_zeitSo = request.form['from_zeitSo']
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
            driver_offer.creator.append(current_user)
            db.session.commit()
            return redirect('/driverOffer')
        except:
            return 'An Error occured, while trying to add your offer :('
    else:
        allDriverOffers = DriverOffers.query.order_by(DriverOffers.id).all()
        return render_template('driverOffer.html', view_name ='Driver Offer', allDriverOffers=allDriverOffers, form=form)

@driverOffer.route('/deleteDriverOffer/<int:id>')
def delete(id):
    driverOffer_to_delete = DriverOffers.query.get_or_404(id)
    try:
        db.session.delete(driverOffer_to_delete)
        db.session.commit()
        return redirect('/driverOffer')
    except:
        return 'The offer could not be deleted :('
