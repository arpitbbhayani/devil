import app
import os, json, datetime, bson
from flask import Blueprint, g
from flask import render_template, request, jsonify, flash, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required

from app.exceptions import *
from app.oauth import OAuthSignIn

from app.db import db
from app.mail import emails
from app.models.user import LUser, User

mod = Blueprint('pages', __name__, )

@mod.route('/', methods=["GET"])
def index():
    next_url = request.args.get('next') or url_for('pages.index')
    return render_template('index.html', next_url=next_url)

@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))

@mod.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('pages.index'))

    next_url = request.args.get('next') or url_for('pages.index')
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize(next_url)

@mod.route('/callback/<provider>')
def oauth_callback(provider):
    next_url = request.args.get('next') or url_for('pages.index')
    if not g.user.is_anonymous:
        return redirect(url_for('pages.index'))
    oauth = OAuthSignIn.get_provider(provider)

    social_id, fname, lname, email = oauth.callback(next_url)

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('pages.index'))
    user = LUser.query.filter_by(email=email).first()
    if not user:
        user = LUser(id=str(bson.ObjectId()), social_id=social_id, fname=fname, lname=lname, email=email)
        db.session.add(user)
        db.session.commit()
        User.create(user.id)

        emails.welcome_email(user.fname, user.email)
    else:
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()

    login_user(user, True)
    return redirect(next_url)
