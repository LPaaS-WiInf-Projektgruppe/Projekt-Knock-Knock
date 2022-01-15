
from flask import Flask, render_template, Blueprint

impressum = Blueprint('impressum', __name__)

@impressum.route('/impressum')
def about_func():
    return render_template('impressum.html', view_name ='Impressum')