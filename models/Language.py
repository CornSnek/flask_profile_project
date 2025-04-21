import models
from sqlalchemy import Column, Integer, String

class Language(models.db.DBBase):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True, nullable = False)