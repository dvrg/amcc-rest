from flask_mail import Message
from threading import Thread
from flask import current_app
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template):
    app = current_app._get_current_object()
    msg = Message(
        current_app.config["MAIL_SUBJECT_PREFIX"] + "|" + subject,
        sender=current_app.config["MAIL_SENDER"],
        recipients=[to],
        html=template,
    )
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
