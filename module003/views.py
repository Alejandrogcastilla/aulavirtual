from flask import Blueprint, render_template
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, Response
from flask_login import login_required, current_user
from models import get_db, User, Course, Follow, Post, Assignment, Entrega
from sqlalchemy import or_, and_
from module003.forms import *
import datetime
from werkzeug.utils import secure_filename
from werkzeug import FileWrapper

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module003.route('/')
@login_required
def module003_index():
        if current_user.profile in ('admin','staff','student'):
            follows = Follow.query.filter_by(user_id=current_user.id)
            return render_template("module003_assignment.html",module="module003", rows=follows)
        else:
            flash("Access denied!")
            #abort(404,description="Access denied!")
            return redirect(url_for('index'))


@module003.route('/<course_id>/', methods=['POST', 'GET'])
@login_required
def module003_assignment_course(course_id):
    form = AssigmentForm()
    course = Course.query.filter_by(id=course_id).first()
    follow = Follow.query.filter(and_(Follow.course_id==course_id,
                                              Follow.user_id==current_user.id)).first()
    assignments = Assignment.query.filter_by(course_id=course_id)
    if follow:
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.never_expire.data:
                    assignment = Assignment(
                            course_id = course_id,
                            author_id = current_user.id,
                            name = form.name.data,
                            descripcion= form.descripcion.data)
                else:
                    assignment = Assignment(
                            course_id = course_id,
                            author_id = current_user.id,
                            name = form.name.data,
                            descripcion = form.descripcion.data,
                            date_expire = datetime.datetime.combine(form.date_expire.data, form.time_expire.data))
                try:
                    db.session.add(assignment)
                    db.session.commit()
                    flash("Assignment created")
                except:
                    db.session.rollback()
                    flash("Error creating Assignment!")
            return redirect(url_for('module003.module003_assignment_course', course_id=course.id))
        else:
            if current_user.profile in ('admin','staff','student'):
                follows = Follow.query.filter_by(user_id=current_user.id)
                return render_template("module003_assignment_especifico.html", form=form, module="module003", rows=follows, course=course, assignments=assignments )
            else:
                flash("Access denied!")
                return redirect(url_for('index'))
    else:
        flash("Access denied!")
#       abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module003.route('/<course_id>/<assignment_id>/', methods=['POST', 'GET'])
@login_required
def module003_assignment_send(course_id, assignment_id):
    follow = Follow.query.filter(and_(Follow.course_id==course_id,
                                              Follow.user_id==current_user.id)).first()

    course = Course.query.filter_by(id=course_id).first()
    if follow:
        assignment = Assignment.query.filter_by(id=int(assignment_id)).first()
        if course.user_id == current_user.id:
            entrega = Entrega.query.filter_by(assignment_id=int(assignment_id))
            return render_template("module003_correccion_ejercicio.html", module='module003', assignment=assignment, entrega = entrega)
        else:
            entrega = Entrega.query.filter(and_(Entrega.assignment_id==assignment_id, Entrega.user==current_user.id)).first()
            return render_template("module003_upload_assignment.html", module='module003', assignment=assignment, entrega = entrega, assignment_id=assignment_id)

    else:
        flash("Access denied!")
#       abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module003.route('/<course_id>/<assignment_id>/upload', methods=['POST'])
@login_required
def module003_upload(course_id, assignment_id):
    if request.method == 'POST':
        file_contents = request.files['file']
        newfile = Entrega(name=file_contents.filename, file=file_contents.read(), user=current_user.id, assignment_id=request.form['tarea'])
        db.session.add(newfile)
        db.session.commit()
        return f'Uploaded file {file_contents.filename}'

    return redirect(url_for('index'))




@module003.route('/test')
def module003_test():
    return 'OK'