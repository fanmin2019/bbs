from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models import language
from models.language import Language
from routes import *

from models.board import Board


main = Blueprint('language', __name__)


@main.route("/")
def index():
    ls = Language.all()
    print(ls)
    user = current_user()
    return render_template('lang.html', ls=ls, tranlates=ls, user=user)


@main.route("/lang_add", methods=["POST"])
def lang_add():
    form = request.form
    u = current_user()
    m = Language.new(form)
    return redirect(url_for('language.index'))

