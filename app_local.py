from flask import Flask

import secret
# import config
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes, mail
from routes.blog import main as blog_routes
from routes.resetpass import main as reset_pass_routes
from utils import log


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = secret.secret_key
    # 现在 mysql root 默认用 socket 来验证而不是密码
    # uri = 'mysql+pymysql://root@127.0.0.1/bbs?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'
    uri = 'mysql+pymysql://root:test@127.0.0.1/bbs'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'fanmin2010@gmail.com'
    app.config['MAIL_PASSWORD'] = secret.mail_password

    mail.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    """
    在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
    蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
    用法如下
    """
    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(blog_routes, url_prefix='/blog')
    app.register_blueprint(reset_pass_routes, url_prefix='/search_pass')
    # app.register_blueprint(mail_routes, url_prefix='/message')


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
