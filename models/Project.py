import models
from sqlalchemy import Column, Integer, Text

class Project(models.db.DBBase):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    content = Column(Text, nullable = False)

