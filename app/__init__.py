from flask import Flask
from flask import jsonify
from flask.ext.cors import CORS

app = Flask(__name__)
app.debug = True

cors = CORS(app, resources={r"/quoracard/process": {"origins": "*"}})

app.config.from_object('app.config')

from app.views import pages
from app.views import conteno
from app.views import quora

from app.quora_widget_api.app.quora import views as quora_api

app.register_blueprint(pages.mod)
app.register_blueprint(conteno.mod, url_prefix='/conteno')
app.register_blueprint(quora.mod, url_prefix='/quora')
app.register_blueprint(quora_api.mod, url_prefix='/quoracard')

from app.exceptions import DevilException

@app.errorhandler(DevilException)
def handle_invalid_usage(error):
    return jsonify(error=error.to_dict()), 500


from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = '/login'

from app.models.user import Profile

@login_manager.user_loader
def load_user(id):
    try:
        user = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        user = None
    return user
