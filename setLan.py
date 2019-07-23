from sqlalchemy import create_engine

#import secret
from app import configured_app
from models.base_model import db
from models.blog import Blog
from models.blog_comment import BlogComment
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.language import Language


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    # uri = 'mysql+pymysql://root@127.0.0.1/?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'
    uri = 'mysql+pymysql://root:test@127.0.0.1'
    e = create_engine(uri, echo=True)

    with e.connect() as c:
        c.execute('USE bbs')

    # db.metadata.create_all(bind=e)


def generate_fake_date():

    # Language.del
    Language.deleteAll()
    form = dict(
        filedName='createTopic',
        labelName='发表话题',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='createTopic',
        labelName='新規質問',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='createTopic',
        labelName='New Topic',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='homepage',
        labelName='Homepage',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='homepage',
        labelName='主页',
        language='cn'
    )

    Language.new(form)

    form = dict(
        filedName='homepage',
        labelName='ホームページ',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='blog',
        labelName='ブログ',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='blog',
        labelName='Blog',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='blog',
        labelName='博客',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='logout',
        labelName='ログアウト',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='logout',
        labelName='Signout',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='logout',
        labelName='登出',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='all_topic',
        labelName='全部のトピック',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='all_topic',
        labelName='All topic',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='all_topic',
        labelName='全部话题',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='spin',
        labelName='人気トピック',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='spin',
        labelName='Hot',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='spin',
        labelName='精品',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='qa',
        labelName='Q&A',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='qa',
        labelName='Q&A',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='qa',
        labelName='问答',
        language='cn'
    )
    Language.new(form)

    form = dict(
        filedName='share',
        labelName='共有',
        language='jp'
    )
    Language.new(form)

    form = dict(
        filedName='share',
        labelName='Share',
        language='en'
    )
    Language.new(form)

    form = dict(
        filedName='share',
        labelName='分享',
        language='cn'
    )
    Language.new(form)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
