from profSearch import db
from profSearch.models import *

def search_professor(query):
    profs = db.session.query(Professor).filter(Professor.lName.ilike('%' + query + '%')).all()
    return profs

def search_classroom(query):
    classrooms = db.session.query(Classroom, Campus).join(Campus).options(db.joinedload(Campus.name))\
        .with_entities(Classroom.place,Campus.name, Classroom.campus_id, Classroom.id)\
        .filter(Classroom.place.ilike('%' + query + '%'))\
        .order_by(Classroom.place,Campus.name)\
        .all()
    return classrooms


def get_prof_schedule(prof_id):
    name = db.session.query(Professor).filter(Professor.id == prof_id).first()
    p = db.session.query(Lesson, Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .join(Week_type, Weekday, Subject, Subject_type, Classroom, Campus) \
        .options(db.joinedload(Lesson.groups).load_only('title')) \
        .filter(Lesson.prof_id == prof_id) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .with_entities(Lesson, Week_type.title, Weekday.name, Classroom, Subject.title, Subject_type.name,
                       Campus.name) \
        .all()
    json = {'fName' : name.fName,
            'lName' : name.lName,
            'mName' : name.mName,
            'data':{}}

    for lssn in p:
        json['data'].setdefault(lssn[1], {})
        json['data'][lssn[1]].setdefault(lssn[2], [])
        json['data'][lssn[1]][lssn[2]].append({
                                       'subGroup': lssn[0].subGroup,
                                       'title': lssn[4],
                                       'groups': [gr.title for gr in lssn[0].groups],
                                       'subject_type': lssn[5]})

        if lssn[0].tStart or lssn[0].tEnd:
            json['data'][lssn[1]][lssn[2]][-1]['sTime'] = lssn[0].tStart.strftime('%H:%M')
            json['data'][lssn[1]][lssn[2]][-1]['eTime'] = lssn[0].tEnd.strftime('%H:%M')
        else:
            json['data'][lssn[1]][lssn[2]][-1]['sTime'] = json['data'][lssn[1]][lssn[2]][-1]['eTime'] = ''

        if lssn[6] == 'N/A':
            json['data'][lssn[1]][lssn[2]][-1]['campus'] = ''
        else:
            json['data'][lssn[1]][lssn[2]][-1]['campus'] = lssn[6]
        if lssn[3].place == 'N/A':
            json['data'][lssn[1]][lssn[2]][-1]['classroom'] = ''
        else:
            json['data'][lssn[1]][lssn[2]][-1]['classroom'] = lssn[3]

    return json

def get_campus_list():
    p = db.session.query(Campus).filter(Campus.name != 'N/A').all()
    return p

def get_classroom_list(campus_id):
    p = db.session.query(Classroom) \
        .filter(db.and_(Classroom.campus_id == campus_id, Classroom.place != 'N/A'))\
        .order_by(Classroom.place) \
        .all()

    return p

def get_classroom_schedule(classroom_id):
    place = db.session.query(Classroom.place,Campus.name).join(Campus).filter(Classroom.id == classroom_id).first()

    p = db.session.query(Classroom, Professor, Lesson, Week_type, Weekday, Subject, Subject_type) \
        .options(db.joinedload(Classroom.lessons), db.joinedload(Lesson.groups).load_only('title')) \
        .join(Lesson, Subject, Weekday, Week_type, Subject_type, Professor) \
        .filter(Classroom.id == classroom_id) \
        .order_by(Lesson.isEvenWeek, Lesson.dayOfWeek, Lesson.tStart) \
        .with_entities(Lesson, Week_type.title, Weekday.name, Subject.title, Subject_type.name, Professor) \
        .all()
    json = {'place' : place[0],
            'campus' : place[1],
            'data':{}}

    for lssn in p:
        json['data'].setdefault(lssn[1], {})
        json['data'][lssn[1]].setdefault(lssn[2], [])
        json['data'][lssn[1]][lssn[2]].append({
                                       'subGroup': lssn[0].subGroup,
                                       'title': lssn[3],
                                       'groups': [gr.title for gr in lssn[0].groups],
                                       'subject_type': lssn[4]})
        if lssn[0].tStart or lssn[0].tEnd:
            json['data'][lssn[1]][lssn[2]][-1]['sTime'] = lssn[0].tStart.strftime('%H:%M')
            json['data'][lssn[1]][lssn[2]][-1]['eTime'] = lssn[0].tEnd.strftime('%H:%M')
        else:
            json['data'][lssn[1]][lssn[2]][-1]['sTime'] = json['data'][lssn[1]][lssn[2]][-1]['eTime'] = ''
        if lssn[5].lName == 'N/A':
            json['data'][lssn[1]][lssn[2]][-1]['prof'] = ''
        else:
            json['data'][lssn[1]][lssn[2]][-1]['prof'] = lssn[5]

    return json