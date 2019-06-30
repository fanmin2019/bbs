import functools
import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for, render_template, jsonify
import redis

from models.blog import Blog
from models.blog_comment import BlogComment
from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u
# csrf_tokens = dict()
# reset_tokens = dict()
#
#
# def csrf_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         token = request.args['token']
#         u = current_user()
#         if token in csrf_tokens and csrf_tokens[token] == u.id:
#             csrf_tokens.pop(token)
#             return f(*args, **kwargs)
#         else:
#             abort(401)
#
#     return wrapper
#
#


# 把 csrf_token 存到 redis 中。确保多个 gunicorn worker 下，csrf 攻击不起作用
cache_csrf = redis.StrictRedis()
# cache_reset_token = redis.StrictRedis()


def new_csrf_token():
    u = current_user()
    uid = u.id
    token = str(uuid.uuid4())
    k = 'csrf_token_{}'.format(token)
    cache_csrf.set(k, uid)
    print('new_csrf_token', k)
    return token


def new_csrf_token_key(key):
    token = str(uuid.uuid4())
    k = 'csrf_token_{}'.format(token)
    cache_csrf.set(k, key)
    print('new_csrf_token', k)
    return token


def new_reset_token(uid):
    token = str(uuid.uuid4())
    k = 'reset_token_{}'.format(token)
    cache_csrf.set(k, uid)
    return token


def username_to_reset(token):
    k = 'reset_token_{}'.format(token)
    print("username_to_reset", k)
    v = cache_csrf.get(k)
    return v.decode('utf-8')


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        username = request.form['username']
        u = current_user()
        k = 'csrf_token_{}'.format(token)
        print("csrf_required", k, username)
        # if token in csrf_tokens and csrf_tokens[token] == u.id:
        if cache_csrf.exists(k):
            v = cache_csrf.get(k)
            print("v", v)
            if v is None:
                abort(401)
            else:
                if v.decode('utf-8') == username or v == u.id:
                    return f(*args, **kwargs)
                else:
                    abort(401)
    return wrapper


def reset_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        k = 'reset_token_{}'.format(token)
        print("reset_required", k)
        if cache_csrf.exists(k):
            v = cache_csrf.get(k)
            if v is None:
                abort(401)
            else:
                return f(*args, **kwargs)

    return wrapper

# def new_csrf_token():
#     u = current_user()
#     k = 'csrf_token_{}'.format(u.id)
#     token = str(uuid.uuid4())
#     cache_csrf.set(k, token)
#     return token


def login_required(route_function):
    @wraps(route_function)
    def f(*args, **kwargs):
        # 先判断登陆再判断登陆用户是不是当前用户
        # 取得登陆用户
        print("UID NOW", session.get('user_id', ''))
        u = current_user()
        # 如果未登陆重定向到 /login
        if u is not None:
            return route_function(*args, **kwargs)
        else:
            return render_template("index.html")
    return f


def blog_comment_owner_required(route_function):
    @functools.wraps(route_function)
    def f():
        u = current_user()
        comment_id = request.args['id']
        comment_one = BlogComment.one(id=int(comment_id))
        blog_one = Blog.one(id=int(comment_one.blog_id))
        if int(comment_one.user_id) == int(u.id) or int(blog_one.user_id) == int(u.id):
            return route_function()
        else:
            d = dict(
                message="权限不足"
            )
            return jsonify(d)

    return f


def blog_owner_required(route_function):
    @functools.wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            blog_id = request.args['id']
        else:
            blog_id = request.form['id']
        blog_one = Blog.one(id=int(blog_id))
        if int(blog_one.user_id) == int(u.id):
            return route_function()
        else:
            d = dict(
                message="权限不足"
            )
            return jsonify(d)

    return f