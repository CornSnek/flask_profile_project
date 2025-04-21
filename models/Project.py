import models
from sqlalchemy import Column, Integer, Text, String

class Project(models.db.DBBase):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), unique = True, nullable = False)
    content = Column(Text, nullable = False)

