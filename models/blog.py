# blog.py
import time

from sqlalchemy import Column, Unicode, UnicodeText, Integer, String

from models.base_model import SQLMixin, db


class Blog(SQLMixin, db.Model):
    __tablename__ = 'Blog'
    title = Column(Unicode(64), nullable=False)
    title = Column(Unicode(64), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(50), nullable=False)

    # sql_create = '''
    #     CREATE TABLE `Blog` (
    #     `id` INT NOT NULL AUTO_INCREMENT,
    #     `title` VARCHAR(64) NOT NULL,
    #     `content` VARCHAR(2048) NOT NULL,
    #     `user_id` INT NOT NULL,
    #     `user_name` VARCHAR(2048) NOT NULL,
    #     `created_time` INT NOT NULL,
    #     `updated_time` INT NOT NULL,
    #     PRIMARY KEY (`id`)
    # )'''

    # def __init__(self, form):
    #     super().__init__(form)
    #     self.title = form['title']
    #     self.content = form['content']
    #     # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
    #     self.user_id = form['user_id']
    #     self.user_name = form['user_name']
    #     self.created_time = form['created_time']
    #     self.updated_time = form['updated_time']

    @classmethod
    def new(cls, form, u):
        print("blog form", form)
        form['user_id'] = u.id
        form['user_name'] = u.username
        # current_time = int(time.time())
        # form['created_time'] = current_time
        # form['updated_time'] = current_time
        blog = super().new(form)
        return blog
