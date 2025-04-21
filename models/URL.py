import models
from sqlalchemy import Column, Integer, Text, String

class URL(models.db.DBBase):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), unique = True, nullable = False)
    url = Column(Text, nullable = False)
    description = Column(Text, nullable = False)