import app
import os, json, datetime
from flask import Blueprint, g
from flask import render_template, request, jsonify, flash, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required

from app.exceptions import *
from app.oauth import OAuthSignIn

from app.db import db
from app.models.user import LUser, User
from app.models.resources import Resources

from werkzeug import secure_filename

mod = Blueprint('pages', __name__, )


@mod.route('/', methods=["GET"])
def index():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('index.html', next_url=next_url)


@mod.route('/applications', methods=["GET"])
def applications():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('applications.html', next_url=next_url)


@mod.route('/suggestions', methods=["GET"])
def suggestions():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('applications.html', next_url=next_url)

@mod.route('/help', methods=["GET"])
def help():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('help.html', next_url=next_url)


@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))


@mod.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('pages.index'))

    next_url = request.args.get('next') or url_for('pages.index')
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize(next_url)


@mod.route('/callback/<provider>')
def oauth_callback(provider):
    next_url = request.args.get('next') or url_for('pages.index')
    if not g.user.is_anonymous:
        return redirect(url_for('pages.index'))
    oauth = OAuthSignIn.get_provider(provider)

    social_id, fname, lname, email = oauth.callback(next_url)

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('pages.index'))
    user = LUser.query.filter_by(email=email).first()
    if not user:
        user = LUser(social_id=social_id, fname=fname, lname=lname, email=email)
        User.create(user.id)

        db.session.add(user)
        db.session.commit()
    else:
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()

    login_user(user, True)
    return redirect(next_url)


@mod.route('/generate', methods=["GET", "POST"])
@login_required
def generate():
    if request.method == 'POST':
        import bson, base64
        api_key = base64.b64encode(str(bson.ObjectId()))

        user_id = g.user.id
        user = LUser.query.get(user_id)
        user.api_key = api_key
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
        raise ResourceExhaustException('Resources exhausted for media_type : %s\
                and genre : %s' % (media_type, genre))

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
            j = json.loads(inputfile.read())
            Resources.update(app.config.YOUR_ID, media_type, genre, j)

        os.remove(destination)
        return jsonify(hi='Hi')
