from flask import Flask, render_template, Blueprint, request, redirect
from Models import Offers
from extensions import db


create = Blueprint('create', __name__)


@create.route('/create', methods=['POST', 'GET'])
def createOffer():
    if request.method == 'POST':
        content_start = request.form['start']
        content_ende = request.form['ende']
        content_geld = request.form['geld']
        new_offer = Offers(start = content_start, end = content_ende, money = content_geld)
        try:
            db.session.add(new_offer)
            db.session.commit()
            return redirect('/create')
        except:
            return 'An Error occured, while trying to add your offer :('

    else:
        allOffers = Offers.query.order_by(Offers.id).all()
        return render_template('create.html', view_name ='Create', allOffers=allOffers)

@create.route('/delete/<int:id>')
def delete(id):
    offer_to_delete = Offers.query.get_or_404(id)
    try:
        db.session.delete(offer_to_delete)
        db.session.commit()
        return redirect('/create')
    except:
        return 'The offer could not be deleted :('
