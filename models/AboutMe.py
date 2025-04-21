import models
from sqlalchemy import Column, Integer, Text

class AboutMe(models.db.DBBase):
    __tablename__ = 'about_me'
    id = Column(Integer, primary_key=True)
    contents = Column(Text, nullable=False)
