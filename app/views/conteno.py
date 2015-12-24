import app
import os, json, datetime, bson
from flask import Blueprint, g
from flask import render_template, request, jsonify, flash, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required

from app.exceptions import *
from app.oauth import OAuthSignIn

from app.db import db
from app.mail import emails
from app.models.user import LUser, User
from app.models.resources import Resources
from app.models.applications import Applications

from werkzeug import secure_filename

mod = Blueprint('conteno', __name__)

@mod.route('/', methods=["GET"])
@login_required
def index():
    return render_template('conteno_index.html')

@mod.route('/application/<application_id>/edit', methods=["GET", "POST"])
@login_required
def edit_application(application_id):
    next_url = request.args.get('next') or url_for('pages.index')
    if request.method == 'GET':
        app = Applications.fetch_one(application_id)
        if app is None:
            flash('Invalid application')
            return redirect(url_for('pages.applications'))

        if app['user']['id'] != g.user.id:
            flash('Application not found for user')
            return redirect(url_for('pages.applications'))

        return render_template('application.html', next_url=next_url, application=app)
    else:
        application_id = application_id
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        if title is None or description is None:
            flash('Please fill all the mandatory fields.')
            return redirect(url_for('pages.new_application'))

        Applications.update(application_id, title, description, link)

        flash("Application details updated successfully")
        return redirect(url_for('pages.applications'))


@mod.route('/application/<application_id>/delete', methods=["GET"])
@login_required
def delete_application(application_id):
    next_url = request.args.get('next') or url_for('pages.index')
    if request.method == 'GET':
        app = Applications.fetch_one(application_id)

        if app is None:
            flash('Invalid application')
            return redirect(url_for('pages.applications'))

        if app['user']['id'] != g.user.id:
            flash('Application not found for user')
            return redirect(url_for('pages.applications'))

        Applications.delete_one(application_id)
        return redirect(url_for('pages.applications'))


@mod.route('/applications/all', methods=["GET"])
def applications():
    apps = Applications.fetch_all()
    return render_template('applications.html', applications=apps)


@mod.route('/applications/me', methods=["GET"])
@login_required
def user_applications():
    next_url = request.args.get('next') or url_for('pages.index')
    user_id = g.user.id
    apps = Applications.fetch(user_id)
    return render_template('applications.html', next_url=next_url, applications=apps)


@mod.route('/application/new', methods=["GET", "POST"])
@login_required
def new_application():
    next_url = request.args.get('next') or url_for('pages.index')
    if request.method == 'GET':
        return render_template('share.html', next_url=next_url)
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        if title is None or description is None:
            flash('Please fill all the mandatory fields.')
            return redirect(url_for('pages.new_application'))

        Applications.create(g.user, title, description, link)

        flash("Your application is successfully published")
        return redirect(url_for('pages.applications'))


@mod.route('/suggestions', methods=["GET", "POST"])
def suggestions():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        emails.suggestion_email(name, email, message)
        flash('Thank you for contacting us :)')
        return redirect(url_for('pages.index'))
    else:
        return render_template('suggestions.html')


@mod.route('/help', methods=["GET"])
def help():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('help.html', next_url=next_url)


@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))


@mod.route('/generate', methods=["GET", "POST"])
@login_required
def generate():
    if request.method == 'POST':
        import bson, base64
        api_key = base64.b64encode(str(bson.ObjectId()))

        user_id = g.user.id
        user = LUser.query.get(user_id)
        user.api_key = g.user.id + api_key
        db.session.commit()

        flash('Your API key has been generated.')

    return render_template('generate.html')


@mod.route('/<media_type>/<genre>', methods=["GET"])
def fetch(media_type, genre):
    if media_type not in app.config.SUPPORTED_MEDIATYPES:
        raise UnsupportedException('Media type %s is not supported' % media_type)
    if genre not in app.config.SUPPORTED_GENRE:
        raise UnsupportedException('Genre %s is not supported' % genre)

    api_key = request.args.get('api_key')
    if api_key is None:
        raise UnsupportedException('API Key is missing')

    resource = Resources.fetch(api_key, media_type, genre)
    if resource is None:
        raise ResourceExhaustException('Resources exhausted for media_type: %s and genre: %s' % (media_type, genre))

    return jsonify(media_type=media_type, content=resource)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.ALLOWED_EXTENSIONS


@mod.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'GET':
        return render_template('add.html', \
            media_types=app.config.SUPPORTED_MEDIATYPES, \
            genres=app.config.SUPPORTED_GENRE)
    else:
        attachment = request.files['attachment']
        media_type = request.form.get('media_type')
        genre = request.form.get('genre')

        if not media_type or not genre or not attachment:
            flash('Please fill all mandatory fields')
            return redirect(url_for('pages.add'))

        if media_type not in app.config.SUPPORTED_MEDIATYPES:
            raise UnsupportedException('Media type %s is not supported' % media_type)
        if genre not in app.config.SUPPORTED_GENRE:
            raise UnsupportedException('Genre %s is not supported' % genre)

        destination = None
        if attachment and allowed_file(attachment.filename):
            filename = secure_filename(attachment.filename)
            destination = os.path.join(app.config.UPLOAD_FOLDER, filename)
            attachment.save(destination)

        if destination is None:
            raise DevilException('Something went wrong, please upload your \
                content again')

        # Add the content of the file into database
        with open(destination, 'rb') as inputfile:
            items = json.loads(inputfile.read())
            ids, failed_items = Resources.update(media_type, genre, items)

        os.remove(destination)
        return jsonify(inserted_ids=ids, failed_items=failed_items)
