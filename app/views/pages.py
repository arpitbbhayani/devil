import os, json
import app
from flask import Blueprint
from flask import render_template, request, jsonify, flash, url_for, redirect

from app.exceptions import *
from app.models.resources import Resources

from werkzeug import secure_filename

mod = Blueprint('pages', __name__, )

@mod.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@mod.route('/<media_type>/<genre>', methods=["GET"])
def fetch(media_type, genre):
    if media_type not in app.config.SUPPORTED_MEDIATYPES:
        raise UnsupportedException('Media type %s is not supported' % media_type)
    if genre not in app.config.SUPPORTED_GENRE:
        raise UnsupportedException('Genre %s is not supported' % genre)

    resource = Resources.fetch(app.config.YOUR_ID, media_type, genre)
    if resource is None:
        raise ResourceExhaustException('Resources exhausted for media_type : %s \
                and genre : %s' % (media_type, genre))

    return jsonify(media_type=media_type, content=resource)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.ALLOWED_EXTENSIONS


@mod.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'GET':
        return render_template('add.html', media_types=app.config.SUPPORTED_MEDIATYPES, genres=app.config.SUPPORTED_GENRE)
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
            raise DevilException('Something went wrong, please upload your content again')

        # Add the content of the file into database
        with open(destination, 'rb') as inputfile:
            j = json.loads(inputfile.read())
            Resources.update(app.config.YOUR_ID, media_type, genre, j)

        os.remove(destination)
        return jsonify(hi='Hi')
