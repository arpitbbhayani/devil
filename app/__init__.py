from flask import Flask
from flask import jsonify

app = Flask(__name__)

app.config.from_object('app.config')

# from app import views1

from app.views import pages

app.register_blueprint(pages.mod)


from app.exceptions import DevilException

@app.errorhandler(DevilException)
def handle_invalid_usage(error):
    return jsonify(error=error.to_dict()), 500


from flask.ext.login import LoginManager
from app.models.user import LUser

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = '/'

@login_manager.user_loader
def load_user(id):
    return LUser.query.get(id)
