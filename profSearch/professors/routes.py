from flask import Blueprint,redirect,url_for,flash
from flask import render_template
from sqlalchemy import func
from profSearch.db_access import *

professors = Blueprint('professors', __name__, template_folder='templates')

@professors.route("/professors/<int:id>")
def prof_schedule(id):
    json = get_prof_schedule(id)
    for sch in json['data'].values():
        for day in sch.values():
            for lesson in day:
                if (lesson['classroom']):
                    lesson['classroom'] = {'place' : lesson['classroom'].place,
                                           'URI' : url_for('classrooms.classroom_schedule',
                                                            campus_id=lesson['classroom'].campus_id,
                                                            classroom_id=lesson['classroom'].id)}
    return render_template('prof_schedule.html',
                           name="%s %s %s" % (json['lName'], json['fName'],json['mName']),
                           arg=json['data'],
                           title=("%s %c.%c.") % (json['lName'], json['fName'][0],json['mName'][0]) )