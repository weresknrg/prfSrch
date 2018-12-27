from flask import Blueprint, request, jsonify, url_for
from profSearch import db
from profSearch.models import *

api = Blueprint('api', __name__)


@api.route('/api/professors/<int:prof_id>', methods=['POST'])
def get_prof_schedule_json(prof_id):
    name = db.session.query(Professor).filter(Professor.id == prof_id).first()
    p = db.session.query(Lesson, Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .join(Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .options(db.joinedload(Lesson.groups).load_only('title')) \
        .filter(Lesson.prof_id == prof_id) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .with_entities(Lesson, Week_type.title, Weekday.name, Classroom.place, Subject.title, Subject_type.name,
                       Campus.name) \
        .all()
    json = {'fName' : name.fName,
            'lName' : name.lName,
            'mName' : name.mName,
            'data':{}}

    for lssn in p:
        json['data'].setdefault(lssn[1], {})
        json['data'][lssn[1]].setdefault(lssn[2], [])
        json['data'][lssn[1]][lssn[2]].append({'campus': lssn[6],
                                       'classroom':lssn[3],
                                       'sTime': lssn[0].tStart.strftime('%H:%M'),
                                       'eTime': lssn[0].tEnd.strftime('%H:%M'),
                                       'subGroup': lssn[0].subGroup,
                                       'title': lssn[4],
                                       'groups': [gr.title for gr in lssn[0].groups],
                                       'subject_type': lssn[5]})
    return jsonify(json)

@api.route('/api/professors/search', methods=['POST'])
def find_professor():
    data = request.get_json(force=True)
    print(data)
    profs = db.session.query(Professor).filter(Professor.lName.ilike('%' + data['last_name'].strip() + '%')).all()
    output = []
    if profs:
        for p in profs:
            output.append({'fName' : p.fName,
                           'lName' : p.lName,
                           'mName' : p.mName,
                           'URI' : url_for('api.get_prof_schedule_json', prof_id=p.id)})
    return jsonify(output)