import app
from flask import render_template
from flask.ext.mail import Message
from app.mail import mail

from app.decorators import async

@async
def send_async_email(app, msg):
    with app.app.app_context():
        mail.send(msg)

def suggestion_email(name, sender, message):
    msg = Message('Suggestions mail', sender=sender, recipients=app.config.ADMINS)
    msg.body = message
    msg.html = render_template('email/suggestion.html', name=name, sender=sender, message=message)
    send_async_email(app, msg)


def welcome_email(name, email):
    msg = Message('Welcome to Random Cliff', sender='arpit.b.bhayani@gmail.com', recipients=[email])
    msg.body = render_template('email/welcome.html', name=name)
    msg.html = render_template('email/welcome.html', name=name)
    send_async_email(app, msg)
