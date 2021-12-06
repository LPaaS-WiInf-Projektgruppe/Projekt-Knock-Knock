from flask import Flask, render_template, Blueprint, request, redirect
from Models import DriverOffers
from extensions import db
from datetime import datetime

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
def createDriverOffer():
    if request.method == 'POST':
        content_ort = request.form['ort']
        content_fahrzeug = request.form['fahrzeug']
        content_von = request.form['von']
        content_bis = request.form['bis']
        content_preis = request.form['preis']
        content_dauer = request.form['dauer']
        content_position = request.form['position']
        content_radius = request.form['radius']
        content_text = request.form['bemerkungen']
        vonAlsPythonObjekt = datetime.strptime(content_von, '%Y-%m-%dT%H:%M')
        bisAlsPythonObjekt = datetime.strptime(content_bis, '%Y-%m-%dT%H:%M')

        driver_offer = DriverOffers(
            location = content_ort,
            vehicle = content_fahrzeug,
            # created_at = vonAlsPythonObjekt,
            # duration = bisAlsPythonObjekt,
            kilometerpreis = content_preis,
            duration = content_dauer,
            position = content_position,
            radius = content_radius,
            text = content_text
        )
        try:
            db.session.add(driver_offer)
            db.session.commit()
            return redirect('/driverOffer')
        except:
            return 'An Error occured, while trying to add your offer :('
    else:
        allDriverOffers = DriverOffers.query.order_by(DriverOffers.id).all()
        return render_template('driverOffer.html', view_name ='Driver Offer', allDriverOffers=allDriverOffers)

@driverOffer.route('/deleteDriverOffer/<int:id>')
def delete(id):
    driverOffer_to_delete = driverOffers.query.get_or_404(id)
    try:
        db.session.delete(driverOffer_to_delete)
        db.session.commit()
        return redirect('/driverOffer')
    except:
        return 'The offer could not be deleted :('
