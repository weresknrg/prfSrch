from flask import Blueprint, flash, redirect, url_for, render_template
from sqlalchemy import func
from profSearch.models import *

classrooms = Blueprint('classrooms', __name__)

@classrooms.route('/classrooms/<int:id>')
def classroom_schedule(id):
    place = db.session.query(Classroom.place).filter(Classroom.id == id).first()
    if not place:
        flash("Error")
        return redirect(url_for('main.home'))
    p = db.session.query(Classroom,
                         func.to_char(Lesson.tStart, 'HH:MI'), func.to_char(Lesson.tEnd, 'HH:MI'),
                         Week_type.title, Weekday.name, Lesson.subGroup, Classroom.place, Subject.title,
                         Subject_type.name) \
        .options(db.subqueryload(Classroom.lessons),db.subqueryload(Lesson.groups).load_only('id')) \
        .join(Classroom, Subject, Weekday, Week_type, Subject_type) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .filter(Lesson.prof_id == id) \
        .all()
    json = {}

    for lssn in p:
        json.setdefault(lssn[3], {})
        json[lssn[3]].setdefault(lssn[4], [])
        json[lssn[3]][lssn[4]].append({'place': lssn[6],
                                       'sTime': lssn[1],
                                       'eTime': lssn[2],
                                       'subGroup': lssn[5],
                                       'title': lssn[7],
                                       'groups': [gr.id for gr in lssn[0].groups],
                                       'subject_type': lssn[8]})
    return render_template('prof_schedule.html', name=name, arg=json)