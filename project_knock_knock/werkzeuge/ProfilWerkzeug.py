
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint

from extensions import db
from Models import WorkingTime, User
from Fachwerte.work_time import WorkTime as wt
from materialien.profil import Profil



profil = Blueprint('profil', __name__)



@profil.route('/profil')
@login_required
def profil_func():
    curr_user = current_user.username
    result = db.session.query(User, WorkingTime) \
        .join(WorkingTime.driver) \
        .filter_by(username = curr_user) \
        .all()

    work_times = []

    for user, work_time in result:
        work_time = wt(
            work_time.weekday,
            work_time.start_time,
            work_time.end_time
        )
        work_times.append(work_time)
    try:
        user_profile = Profil(result[0][0].username, work_times,  0, result[0][0].username)
    except IndexError:
        pass
        # TODO handle querying when there are no work times

    return render_template("profil.html", view_name='Profil', profile = user_profile)
