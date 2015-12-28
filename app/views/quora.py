import app
import requests
from flask import Blueprint
from flask import render_template, request
from flask.ext.login import login_required

from bs4 import BeautifulSoup

from app.exceptions import *

mod = Blueprint('quora', __name__)

@mod.route('/', methods=["GET"])
def index():
    return render_template('quora_index.html')
