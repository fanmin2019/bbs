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


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    # uri = 'mysql+pymysql://root@127.0.0.1/?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'
    uri = 'mysql+pymysql://root:test@127.0.0.1'
    e = create_engine(uri, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS bbs')
        c.execute('CREATE DATABASE bbs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE bbs')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='min',
        password='123',
        email='fanmin2010@gmail.com',
    )
    u = User.register(form)

    form = dict(
        username='minmin',
        password='123',
        email='fanmin2020@gmail.com',
    )
    u = User.register(form)

    boardList = []
    form = dict(
        title='精华'
    )
    b = Board.new(form)
    boardList.append(b)
    form = dict(
        title='问答'
    )
    b = Board.new(form)
    boardList.append(b)
    form = dict(
        title='分享'
    )
    b = Board.new(form)
    boardList.append(b)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()

    for i in range(10):
        print('begin topic <{}>'.format(i))
        topic_form = dict(
            title='markdown demo' + boardList[i % 3].title,
            board_id=boardList[i % 3].id,
            content=content
        )
        t = Topic.new(topic_form, u.id)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
        )
        for j in range(5):
            Reply.new(reply_form, u.id)


# for blog
    with open('markdown_demo.md', encoding='utf-8') as f:
        demo = f.read()
    #
    form = dict(
        title='markdown demo',
        content=demo,
    )
    Blog.new(form, u)

    form = dict(
        title='blog demo',
        content='blog demo content',
    )
    Blog.new(form, u)

    form = dict(
        content='comment demo content',
        blog_id='1'
    )
    BlogComment.new(form, u)

    with open('demo_comment.md', encoding='utf-8') as f:
        demo_comment = f.read()
    form = dict(
        content=demo_comment,
        blog_id='1'
    )
    BlogComment.new(form, u)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
