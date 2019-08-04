import os
import time
import uuid
import lang
import datetime


from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import login_required, current_user

import json
import redis
from utils import log

cache = redis.StrictRedis()
main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    # form = request.form.to_dict()
    # print("login form", form)
    u = current_user()
    if u is None:
        return render_template("index.html")
    else:
        return redirect(url_for('topic.index'))


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/signup", methods=['GET'])
def signup():
    u = current_user()
    return render_template("register.html", user=u)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        # session.permanent = True

        # 把语言作为一个全局的变量给保存起来
        # 但是仍然有一个问题就是页面里面那么多字句，要怎样实现替换呢
        # 我希望传给jinjia一组字典，然后金甲自己来判断
        language = form['language']
        cache.set("user_language", language)
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))


@main.route("/signout", methods=['GET'])
@login_required
def logout():
    # u = current_user()
    session['user-id'] = 'PPPP'
    print("UID NOW", session.get('user_id', ''))
    session.pop('user-id', None)
    print("UID NOW 2 ", session.get('user_id', ''))
    print(session)
    session.clear()

    return render_template("index.html")


def created_topic(user_id):
    # O(n)
    # ts = Topic.all(user_id=user_id)
    # return ts

    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    # O(k)+O(m*n)
    # rs = Reply.all(user_id=user_id)
    # ts = []
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     ts.append(t)
    # return ts
    #
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.one(id=r.topic_id)
            ts.append(t)

        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)

        return ts


@main.route('/profile')
@login_required
def profile():
    print('running profile route')
    now_time = int(time.time())
    u = current_user()
    created = created_topic(u.id)
    replied = replied_topic(u.id)
    diff = now_time - int(u.created_time)
    # diff = round(diff / 60 / 60)
    # now_time = datetime.datetime.now()
    # created_time = datetime.datetime.fromtimestamp(int(blog.created_time))
    # print("blog_detail_now_time", now_time)
    # diff = now_time - int(blog.created_time)
    # seconds = round(diff / 60 / 60) #秒
    now_time = datetime.datetime.now()
    created_time = datetime.datetime.fromtimestamp(int(u.created_time))
    # print("blog_detail_now_time", now_time)
    # diff = now_time - int(blog.created_time)
    # seconds = round(diff / 60 / 60) #秒
    delta = now_time - created_time
    hours = round(delta.total_seconds() // 3600 - delta.days*24)
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
    return render_template(
        'profile.html',
        user=u,
        other=u,
        created=created,
        replied=replied,
        time=diff
    )


@main.route('/user/<int:id>')
@login_required
def user_detail(id):
    now_time = int(time.time())
    u = User.one(id=id)
    cu = current_user()
    if u is None:
        abort(404)
    else:
        diff = now_time - int(u.created_time)
        diff = round(diff / 60 / 60)
        print(now_time, u.created_time, diff)
        return render_template('profile.html',
                               user=cu, other=u,
                               # time=now_time - u.created_time)
                               time=diff)


@main.route('/image/add', methods=['POST'])
@login_required
def avatar_add():
    file: FileStorage = request.files['avatar']

    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
@login_required
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)
