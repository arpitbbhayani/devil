from flask import Blueprint

from flask import render_template, request, redirect
from flask import url_for, make_response

mod = Blueprint('pages', __name__, )

@mod.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
