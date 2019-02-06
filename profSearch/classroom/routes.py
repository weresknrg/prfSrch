from flask import Blueprint, flash, redirect, url_for, render_template
from sqlalchemy import func, and_
from profSearch.db_access import *

classrooms = Blueprint('classrooms', __name__, template_folder='templates')

@classrooms.route('/campus/')
def campus_list():
    p = get_campus_list()
    return render_template('campus_list.html', campuses=p)

@classrooms.route('/campus/<int:id>/')
@classrooms.route('/campus/<int:id>/classrooms')
def classroom_list(id):
    p = get_classroom_list(id)
    return render_template('room_list.html', classes=p)

@classrooms.route('/classrooms/<int:classroom_id>')
def classroom_schedule(classroom_id):
    json = get_classroom_schedule(classroom_id=classroom_id)
    for sch in json['data'].values():
        for day in sch.values():
            for lesson in day:
                if (lesson['prof']):
                    lesson['prof'] = {'lName': lesson['prof'].lName,
                                      'fName': lesson['prof'].fName,
                                      'mName': lesson['prof'].mName,
                                      'URI': url_for('professors.prof_schedule',
                                                      id=lesson['prof'].id)
                                      }

    return render_template('room_schedule.html', arg=json['data'], place=(json['place'], json['campus']))