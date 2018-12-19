from flask import Blueprint,redirect,url_for,flash
from profSearch import db
from profSearch.models import *
from flask import render_template
from sqlalchemy import func

professors = Blueprint('professors', __name__)

@professors.route("/professors/<int:id>")
def prof_schedule(id):
    name = db.session.query(Professor.lName,Professor.fName,Professor.mName).filter(Professor.id == id).first()
    if not name:
        flash("Error")
        return redirect(url_for('main.home'))
    p = db.session.query(Lesson,
                         func.date_format(Lesson.tStart, '%H:%i'), func.DATE_FORMAT(Lesson.tEnd, '%H:%i'),
                         Week_type.title, Weekday.name, Lesson.subGroup, Classroom.place, Subject.title,
                         Subject_type.name,Campus.name) \
        .options(db.subqueryload(Lesson.groups).load_only('id')) \
        .join(Classroom, Subject, Weekday, Week_type, Subject_type, Campus) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .filter(Lesson.prof_id == id) \
        .all()
    json = {}

    for lssn in p:
        json.setdefault(lssn[3], {})
        json[lssn[3]].setdefault(lssn[4], [])
        json[lssn[3]][lssn[4]].append({'place': "%s %s" % (lssn[6],lssn[9]),
                                       'sTime': lssn[1],
                                       'eTime': lssn[2],
                                       'subGroup': lssn[5],
                                       'title': lssn[7],
                                       'groups': [gr.id for gr in lssn[0].groups],
                                       'subject_type': lssn[8]})
    return render_template('prof_schedule.html', name=name, arg=json, title=("%s %c.%c.") % (name[0], name[1][0],name[2][0]) )