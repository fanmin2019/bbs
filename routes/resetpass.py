from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

import flask_mail
from routes import *
mail = flask_mail.Mail()
main = Blueprint('search_pass', __name__)


@main.route("/index")
def index():
    return render_template('reset_your_password.html')


@main.route("/reset", methods=["POST"])
def reset():
    form = request.form
    mail_subject = "Reset your password for fan-min.com"
    ps_token = new_reset_token(form['username'])
    email_addr = form['email']
    mail_body = "Please Reset your password by access the link below  http://localhost:2000/search_pass/reset_pwd?token={}".format(ps_token)
    msg = mail.send_message(
        mail_subject,
        sender='fanmin2010@gmail.com',
        recipients=[email_addr],
        body=mail_body
    )
    print("msg", msg)
    return render_template('index.html')


@main.route("/reset_pwd")
@reset_required
def reset_pwd():
    print("reset_pwd start")
    # form = request.form

    username = username_to_reset(request.args['token'])
    token = new_csrf_token_key(username)
    print("reset_required username", username, token)
    return render_template('reset_password.html', token=token)


# @main.route("/reset_password")
# @reset_required
# def reset_password():
#     form = request.form
#     u = current_user()
#     return render_template('index.html')


@main.route("/update_password", methods=["POST"])
@csrf_required
def update_password():
    print("update_password")
    form = request.form
    new_password = User.salted_password(form['new-password'])
    username = form['username']
    u = User.one(username=username)
    uid = u.id
    print("new_password", new_password,username, uid)
    User.update(id=uid, password=new_password)

    return render_template('index.html')

