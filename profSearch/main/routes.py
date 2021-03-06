from flask import Blueprint, Markup
from flask import render_template,request,redirect,flash, url_for
from profSearch.db_access import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route("/")
@main.route("/home/", methods=['GET', 'POST'])
def home():
    q = request.args.get('q', None)
    if q:
        profs = search_professor(q)
        if not profs:
            flash('No results','error')
            return redirect(url_for('main.home'))
        elif len(profs) == 1:
            return redirect(url_for('professors.prof_schedule', id=profs[0].id))
        else:
            for p in profs:
                flash(Markup("<a href=\"/professors/%i\" class=\"alert-link\">%s %s %s</a>" % (p.id,p.lName, p.fName, p.mName)), 'success')
            return redirect(url_for('main.home'))
    return render_template('home.html')

@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


