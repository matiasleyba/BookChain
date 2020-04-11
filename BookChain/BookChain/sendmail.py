from flask import Flask , render_template
from flask_mail import Mail, Message
from BookChain import app
import os


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'bookchainnotify@gmail.com',
    "MAIL_PASSWORD": '54156795'
    #"MAIL_USERNAME": os.environ['EMAIL_USER'],
    #"MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

class EmailController:

    @staticmethod
    def SendEmail(mail_user):
        msg = Message(subject="BookChain - Notificacion",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[mail_user]) # replace with your email for testing
        msg.html= render_template("email.html")
        mail.send(msg)