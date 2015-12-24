from flask import Flask
from flask import jsonify

app = Flask(__name__)

app.config.from_object('app.config')

from app.views import pages
from app.views import conteno
from app.views import quora

app.register_blueprint(pages.mod)
app.register_blueprint(conteno.mod, url_prefix='/conteno')
app.register_blueprint(quora.mod, url_prefix='/quora')

from app.exceptions import DevilException

@app.errorhandler(DevilException)
def handle_invalid_usage(error):
    return jsonify(error=error.to_dict()), 500


from flask.ext.login import LoginManager
from app.models.user import LUser

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(id):
    return LUser.query.get(id)
