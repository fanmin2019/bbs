import time
from models.user import User
from sqlalchemy import Column, Unicode, UnicodeText, Integer, String

from models.base_model import SQLMixin, db


class BlogComment(SQLMixin, db.Model):
    """
    评论类
    """
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    blog_id = Column(Integer, nullable=False)
    user_name = Column(String(50), nullable=False)

    # sql_create = '''
    #     CREATE TABLE `BlogComment` (
    #     `id` INT NOT NULL AUTO_INCREMENT,
    #     `content` VARCHAR(2048) NOT NULL,
    #     `blog_id` INT NOT NULL,
    #     `user_id` INT NOT NULL,
    #     `user_name` VARCHAR(2048) NOT NULL,
    #     `created_time` INT NOT NULL,
    #     `updated_time` INT NOT NULL,
    #     PRIMARY KEY (`id`)
    # )'''

    # def __init__(self, form, user_id=-1):
    #     super().__init__(form)
    #     self.content = form.get('content', '')
    #     # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
    #     self.user_id = form.get('user_id', user_id)
    #     self.user_name = form.get('user_name', '')
    #     self.blog_id = int(form.get('blog_id', -1))
    #     self.created_time = form.get('created_time', -1)
    #     self.updated_time = form.get('updated_time', -1)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, u):
        form['user_id'] = u.id
        form['user_name'] = u.username
        c = super().new(form)
        return c

    @classmethod
    def delete_all(cls, blog_id):
        cs = BlogComment.all(blog_id=blog_id)
        for c in cs:
            c.delete()
