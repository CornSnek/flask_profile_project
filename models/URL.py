import models
from sqlalchemy import Column, Integer, Text

class URL(models.db.DBBase):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    url = Column(Text, nullable = False)
    description = Column(Text, nullable = False)