from flask import Blueprint,redirect,url_for,flash
from profSearch import db
from profSearch.models import *
from flask import render_template
from sqlalchemy import func

professors = Blueprint('professors', __name__, template_folder='templates')

@professors.route("/professors/<int:id>")
def prof_schedule(id):
    name = db.session.query(Professor).filter(Professor.id == id).first()
    if not name:
        flash("Error")
        return redirect(url_for('main.home'))
    p = db.session.query(Lesson, Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .join(Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .options(db.joinedload(Lesson.groups).load_only('title')) \
        .filter(Lesson.prof_id == id) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .with_entities(Lesson, Week_type.title, Weekday.name, Classroom, Subject.title, Subject_type.name,
                       Campus) \
        .all()
    json = {}

    for lssn in p:
        json.setdefault(lssn[1], {})
        json[lssn[1]].setdefault(lssn[2], [])
        json[lssn[1]][lssn[2]].append({'campus': lssn[6],
                                       'classroom':lssn[3],
                                       'sTime': lssn[0].tStart.strftime('%H:%M'),
                                       'eTime': lssn[0].tEnd.strftime('%H:%M'),
                                       'subGroup': lssn[0].subGroup,
                                       'title': lssn[4],
                                       'groups': [gr.title for gr in lssn[0].groups],
                                       'subject_type': lssn[5]})
    return render_template('prof_schedule.html',
                           name="%s %s %s" % (name.lName, name.fName,name.mName),
                           arg=json,
                           title=("%s %c.%c.") % (name.lName, name.fName[0],name.mName[0]) )