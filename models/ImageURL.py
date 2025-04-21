import models
from sqlalchemy import Column, Integer, Text

class ImageURL(models.db.DBBase):
    __tablename__ = 'image_urls'
    id = Column(Integer, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    url = Column(Text, nullable = False)
    description = Column(Text, nullable = False)