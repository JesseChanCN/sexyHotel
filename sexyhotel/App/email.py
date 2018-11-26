from flask import current_app,render_template
from flask_mail import Mail, Message
import threading
from .extensions import mail

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, to, temname, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to],
 sender = current_app.config['MAIL_USERNAME'])
    msg.html = render_template('email/'+temname+'.html',**kwargs)
    t = threading.Thread(target=async_send_mail, args=(app, msg))
    t.start()
    return '发送邮件成功～'


