# blog.py
import time

from sqlalchemy import Column, Unicode, UnicodeText, Integer, String

from models.base_model import SQLMixin, db


class Language(SQLMixin, db.Model):
    __tablename__ = 'Language'
    filedName = Column(Unicode(64), nullable=False)
    labelName = Column(Unicode(64), nullable=False)
    language = Column(UnicodeText, nullable=False)

