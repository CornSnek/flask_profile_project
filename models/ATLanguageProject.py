import models
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

class ATLanguageProject(models.db.DBBase):
    __tablename__ = 'at_languages_projects'
    id = Column(Integer, primary_key = True)
    language_id = Column(Integer, ForeignKey('languages.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('language_id', 'project_id', name='uix_language_project'),)

