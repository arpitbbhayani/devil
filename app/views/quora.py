from flask import Blueprint
from flask import render_template

mod = Blueprint('quora', __name__)

@mod.route('/', methods=["GET"])
def index():
    return render_template('quora_index.html')
