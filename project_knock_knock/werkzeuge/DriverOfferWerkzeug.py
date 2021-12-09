from flask import Flask, render_template, Blueprint, request, redirect
from flask_user import current_user
from Models import DriverOffers, WorkingTime
from extensions import db
from datetime import datetime, timedelta

from forms.driverOffer_form import DriverOfferForm

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
def createDriverOffer():

    form = DriverOfferForm()

    if form.validate_on_submit():
        content_ort = request.form['ort']
        content_fahrzeug = request.form['fahrzeug']
        content_von = request.form['start_date']
        content_bis = request.form['end_date']
        content_preis = request.form['preis']
        content_radius = request.form['radius']
        content_text = request.form['bemerkungen']
        vonAlsPythonObjekt = datetime.strptime(content_von, '%Y-%m-%dT%H:%M')
        bisAlsPythonObjekt = datetime.strptime(content_bis, '%Y-%m-%dT%H:%M')
        print("hello world")

        # i = 0
        # for results in request.form:
        #     if (results == "from_zeitMo" or results == "from_zeitDi" or results == "from_zeitMi" or \
        #         results == "from_zeitDo" or results == "from_zeitFr" or results == "from_zeitSa" or \
        #         results == "from_zeitSo"):
        #
        #         bis = datetime.strptime(request.form[results],'%H:%M')
        #         bis += timedelta(hours=8)
        #         bis.strftime('%H:%M')
        #         working_time = WorkingTime(
        #             weekday = i,
        #             start_time = request.form[results],
        #             end_time = bis
        #         )
        #
        #         working_time.driver.append(current_user)
        #         db.session.add(working_time)
        #
        #         i+=1

        driver_offer = DriverOffers(
            location = content_ort,
            vehicle = content_fahrzeug,
            start_time = vonAlsPythonObjekt,
            end_time = bisAlsPythonObjekt,
            kilometerpreis = content_preis,
            radius = content_radius,
            text = content_text
        )
        # try:

        # print(driver_offer)
        db.session.add(driver_offer)
        db.session.commit()
        return redirect('/driverOffer')
        # except:
        # return 'An Error occured, while trying to add your offer :('
    else:
        allDriverOffers = DriverOffers.query.order_by(DriverOffers.id).all()
        return render_template('driverOffer.html', view_name ='Driver Offer', allDriverOffers=allDriverOffers, form = form)

@driverOffer.route('/deleteDriverOffer/<int:id>')
def delete(id):
    driverOffer_to_delete = DriverOffers.query.get_or_404(id)
    try:
        db.session.delete(driverOffer_to_delete)
        db.session.commit()
        return redirect('/driverOffer')
    except:
        return 'The offer could not be deleted :('
