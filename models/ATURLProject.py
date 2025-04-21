import models
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class ATURLProject(models.db.DBBase):
    __tablename__ = 'at_urls_projects'
    id = Column(Integer, primary_key = True)
    url_id = Column(Integer, ForeignKey('urls.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    sort_order = Column(Integer, nullable=False, server_default='0')
    __table_args__ = (UniqueConstraint('url_id', 'project_id', name='uix_url_project'),)

