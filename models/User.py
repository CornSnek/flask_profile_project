import models
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin

class User(models.db.DBBase, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(32), unique = True, nullable = False)
    password_hash = Column(String(200), nullable = False)