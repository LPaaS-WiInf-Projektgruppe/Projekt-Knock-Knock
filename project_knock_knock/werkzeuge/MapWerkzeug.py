from flask import Flask, render_template, Blueprint, request, redirect


map = Blueprint('map', __name__)


@map.route('/map', methods=['GET'])
def createMap():

        return render_template('map.html', view_name ='Map')
