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
