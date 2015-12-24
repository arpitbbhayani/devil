import app
from flask import Blueprint
from flask import render_template, request
from flask.ext.login import login_required

from app.exceptions import *

mod = Blueprint('quora', __name__)

@mod.route('/', methods=["GET"])
@login_required
def index():
    return render_template('quora_index.html')


@mod.route('/process', methods=["GET"])
@login_required
def process():
    print request.args
    return 'Generate data for ' + request.args['url']
