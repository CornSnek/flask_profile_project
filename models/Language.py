import models
from sqlalchemy import Column, Integer, Text

class Language(models.db.DBBase):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key = True)
    name = Column(Text, unique = True, nullable = False)