import models
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

class ATImageURLProject(models.db.DBBase):
    __tablename__ = 'at_image_urls_projects'
    id = Column(Integer, primary_key = True)
    image_url_id = Column(Integer, ForeignKey('image_urls.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    sort_order = Column(Integer, nullable=False, server_default='0')
    __table_args__ = (UniqueConstraint('image_url_id', 'project_id', name='uix_image_url_project'),)

