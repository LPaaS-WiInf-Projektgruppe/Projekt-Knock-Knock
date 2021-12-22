from flask import Flask, render_template, Blueprint, request, redirect
from flask_user import current_user, login_required
from Models import DriverOffers, WorkingTime
from extensions import db
from datetime import datetime, timedelta

from forms.driverOffer_form import DriverOfferForm
from forms.search_drive_offer_form import SearchDriveOfferForm

driverOffer = Blueprint('driverOffer', __name__)


@driverOffer.route('/driverOffer', methods=['POST', 'GET'])
@login_required
def driver_offer():
    form = SearchDriveOfferForm()

    allDriverOffers = DriverOffers.query.order_by(DriverOffers.id).all()
    return render_template(
        'driverOffer.html',
        view_name ='Driver Offer',
        allDriverOffers=allDriverOffers,
        form = form
        )


@driverOffer.route('/deleteDriverOffer/<int:id>')
def delete(id):
    ''' delete the drive offer specified by the id in the url
    :param id int: the id of the drive offer to delete
    '''
    driverOffer_to_delete = DriverOffers.query.get_or_404(id)
    try:
        db.session.delete(driverOffer_to_delete)
        db.session.commit()
        return redirect('/driverOffer')
    except:
        return 'The offer could not be deleted :('



@driverOffer.route('/accept_drive_offer/<int:offer_id>')
def accept_offer(offer_id):
    ''' accept the drive offer specified by the id in the url by adding the id
    of the user who accepted the offer to the respective entry in the drive offer
    "accepted_by" column
    :param offer_id int: the id of the offer to accept
    '''

    # TODO: prevent users from accepting their own offers
    # TODO: contact users who accepted an offer
    # TODO: prevent accepted offers from being deleted
    result = DriverOffers.query.filter_by(id = offer_id).first()
    result.accepted_by = current_user.id
    db.session.commit()

    return redirect('/driverOffer')


@driverOffer.route("/create_drive_offer", methods=["GET", "POST"])
@login_required
def create_drive_offer():
    '''creates a new drive offer
    '''

    form = DriverOfferForm()

    if form.validate_on_submit():
        content_ort = request.form['ort']
        content_fahrzeug = request.form['fahrzeug']
        content_von = request.form['zeit_start']
        content_bis = request.form['zeit_ende']
        content_preis = request.form['preis']
        content_radius = request.form['radius']
        content_text = request.form['bemerkungen']

        formatted_start_zeit = content_von[:10] + '-' + content_von[11:]
        formatted_end_zeit = content_bis[:10] + '-' + content_bis[11:]

        vonAlsPythonObjekt = datetime.strptime(formatted_start_zeit, '%d.%m.%Y-%H:%M')
        bisAlsPythonObjekt = datetime.strptime(formatted_end_zeit, '%d.%m.%Y-%H:%M')


        i = 0
        for results in request.form:
            if (results == "from_zeitMo" or results == "from_zeitDi" or results == "from_zeitMi" or \
                results == "from_zeitDo" or results == "from_zeitFr" or results == "from_zeitSa" or \
                results == "from_zeitSo"):

                bis = datetime.strptime(request.form[results],'%H:%M')
                bis += timedelta(hours=8)
                bis.strftime('%H:%M')
                working_time = WorkingTime(
                    weekday = i,
                    start_time = request.form[results],
                    end_time = bis
                )

                working_time.user.append(current_user)
                db.session.add(working_time)

                i+=1

        driver_offer = DriverOffers(
            location = content_ort,
            vehicle = content_fahrzeug,
            start_time = vonAlsPythonObjekt,
            valid_until = bisAlsPythonObjekt,
            kilometerpreis = content_preis,
            radius = content_radius,
            text = content_text
        )

        try:
            db.session.add(driver_offer)
            driver_offer.creator.append(current_user)
            db.session.commit()
            return redirect('/driverOffer')
        except:
            return 'An Error occured, while trying to add your offer :('

    return render_template(
        "create_drive_offer.html",
        view_name = "Create Driver Offer",
        form = form
    )
