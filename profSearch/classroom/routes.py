from flask import Blueprint, flash, redirect, url_for, render_template
from sqlalchemy import func, and_
from profSearch.models import *

classrooms = Blueprint('classrooms', __name__)

@classrooms.route('/campus/')
def campus_list():
    p = db.session.query(Campus).filter(Campus.name != 'N/A').all()
    return render_template('campus_list.html', campuses=p)

@classrooms.route('/campus/<int:id>/')
@classrooms.route('/campus/<int:id>/classrooms')
def classroom_list(id):
    p = db.session.query(Classroom) \
        .filter(db.and_(Classroom.campus_id == id, Classroom.place != 'N/A'))\
        .order_by(Classroom.place) \
        .all()
    return render_template('room_list.html', classes=p)

@classrooms.route('/campus/<int:campus_id>/classrooms/<int:classroom_id>')
def classroom_schedule(campus_id, classroom_id):
    place = db.session.query(Classroom.place,Campus.name).join(Campus).filter(Classroom.id == classroom_id).first()

    p = db.session.query(Classroom, Professor, Lesson, Week_type, Weekday, Subject, Subject_type) \
        .options(db.joinedload(Classroom.lessons), db.joinedload(Lesson.groups).load_only('title')) \
        .join(Lesson, Subject, Weekday, Week_type, Subject_type, Professor) \
        .filter(Classroom.id == classroom_id) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .with_entities(Lesson, Week_type.title, Weekday.name, Subject.title, Subject_type.name, Professor) \
        .all()
    json = {}

    for lssn in p:
        json.setdefault(lssn[1], {})
        json[lssn[1]].setdefault(lssn[2], [])
        json[lssn[1]][lssn[2]].append({'prof': lssn[5],
                                       'sTime': lssn[0].tStart.strftime('%H:%M'),
                                       'eTime': lssn[0].tEnd.strftime('%H:%M'),
                                       'subGroup': lssn[0].subGroup,
                                       'title': lssn[3],
                                       'groups': [gr.title for gr in lssn[0].groups],
                                       'subject_type': lssn[4]})
    return render_template('room_schedule.html', arg=json, place=place)