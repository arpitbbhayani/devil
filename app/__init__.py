from flask import Flask

app = Flask(__name__)

# from app import views1

from app.views import pages

app.register_blueprint(pages.mod)
