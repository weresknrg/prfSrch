from flask import Blueprint, request, jsonify, url_for
from profSearch.db_access import *

api = Blueprint('api', __name__)

@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@api.route('/api/professors/<int:prof_id>', methods=['POST'])
def prof_schedule_api(prof_id):
    json = get_prof_schedule(prof_id)
    for sch in json['data'].values():
        for day in sch.values():
            for lesson in day:
                if (lesson['classroom']):
                    lesson['classroom'] = {'place' : lesson['classroom'].place,
                                           'URI' : url_for('api.classroom_schedule_api',
                                                            campus_id=lesson['classroom'].campus_id,
                                                            classroom_id=lesson['classroom'].id)}
    return jsonify(json)

@api.route('/api/campus', methods=['POST'], strict_slashes=False)
def campus_list_api():
    campus_list = get_campus_list()
    list = []
    for campus in campus_list:
        list.append({
            'address': campus.address,
            'URI' : url_for('api.classroom_list_api',
                            campus_id=campus.id),
            'name' : campus.name
        })
    return jsonify(list)

@api.route('/api/campus/<int:campus_id>/', methods=['POST'])
@api.route('/api/campus/<int:campus_id>/classrooms', methods=['POST'])
def classroom_list_api(campus_id):
    list = get_classroom_list(campus_id)
    classroom_list = []
    for classroom in list:
        classroom_list.append({
            'name' : classroom.place,
            'URI' : url_for("api.classroom_schedule_api",
                            campus_id = classroom.campus_id,
                            classroom_id = classroom.id)
        })
    return jsonify(classroom_list)

@api.route('/api/campus/<int:campus_id>/classrooms/<int:classroom_id>', methods=['POST'])
def classroom_schedule_api(campus_id, classroom_id):
    json = get_classroom_schedule(classroom_id=classroom_id)
    for sch in json['data'].values():
        for day in sch.values():
            for lesson in day:
                if (lesson['prof']):
                    lesson['prof'] = {'lName': lesson['prof'].lName,
                                      'fName': lesson['prof'].fName,
                                      'mName': lesson['prof'].mName,
                                      'URI': url_for('api.prof_schedule_api',
                                                      prof_id=lesson['prof'].id)
                                      }
    return jsonify(json)


@api.route('/api/professors/search', methods=['POST'])
def find_professor():
    data = request.get_json(force=True)

    profs = search_professor(data['last_name'].strip())
    output = []

    if profs:
        for p in profs:
            output.append({'fName': p.fName,
                           'lName': p.lName,
                           'mName': p.mName})
            if('inner' in data):
                output[-1]['URI'] = url_for('professors.prof_schedule', id=p.id)
            else:
                output[-1]['URI'] = url_for('api.prof_schedule', prof_id=p.id)
    return jsonify(output)

@api.route('/api/classroom/search', methods=['POST'])
def find_classroom():
    data = request.get_json(force=True)
    output = []
    classrooms = search_classroom(data['classroom'].strip())
    if classrooms:
        for c in classrooms:
            output.append({
                'place': c.place,
                'campus':c.name
            })
            if 'inner' in data:
                output[-1]['URI'] = url_for('classrooms.classroom_schedule', classroom_id=c.id)
            else:
                output[-1]['URI'] = url_for('api.classroom_schedule_api', campus_id=c.campus_id,classroom_id=c.id)
    return jsonify(output)