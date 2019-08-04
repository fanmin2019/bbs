import time
import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

import json

from models.language import Language
from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)
cache = redis.StrictRedis()


@main.route("/")
@login_required
def index():
    board_id = int(request.args.get('board_id', -1))
    u = current_user()
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)

    if cache.exists("user_language"):
        language = cache.get("user_language")
        l = language.decode()
    else:
        l = 'en'

    ls = Language.all(language=l)
    tranlates = {

    }

    # if cache.exists("site_translate_list"):
    #     tranlates = cache.get("site_translate_list").decode()
    # else:
    for one in ls:
        print(one)
        tranlates[one.filedName] = one.labelName
    # print("redisにはないので、DBから取得")
    v = json.dumps(tranlates)
    # cache.set(k, v)
    cache.set("site_translate_list", v)

    token = new_csrf_token()
    bs = Board.all()
    # return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=u)
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=u, tranlates=tranlates)


@main.route('/<int:id>')
@login_required
def detail(id):

    v = cache.get("site_translate_list").decode('utf-8')
    tranlates = json.loads(v)
    m = Topic.get(id)
    now_time = int(time.time())
    diff = now_time - int(m.created_time)
    diff = round(diff / 60 / 60)
    u = current_user()

    now_time = datetime.datetime.now()
    created_time = datetime.datetime.fromtimestamp(int(m.created_time))
    delta = now_time - created_time
    hours = round(delta.total_seconds() // 3600 - delta.days * 24)
    minutes = round((delta.total_seconds() % 3600) // 60)
    seconds = round(delta.total_seconds() - minutes * 60)
    if delta.days > 0:
        diff = "{}日{}時間".format(delta.days, hours)
    elif hours > 0 and delta.days <= 0:
        # diff = delta.days + "時間" + delta.minutes + "分"
        diff = "{}時間{}分".format(hours, minutes)
    elif minutes > 0 and hours <= 0:
        # diff = delta.minutes + "分" + delta.seconds + "秒"
        diff = "{}分{}秒".format(minutes, seconds)
    elif delta.minutes <= 0:
        # diff = delta.seconds + "秒"
        diff = "{}秒".format(delta.seconds)

    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, user=u, time=diff, tranlates=tranlates)


@main.route("/delete")
@login_required
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
@login_required
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    v = cache.get("site_translate_list").decode('utf-8')
    tranlates = json.loads(v)
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id, tranlates=tranlates)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))
