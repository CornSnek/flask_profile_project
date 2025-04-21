from typing import Any
import dbconfig
import config
import os
import models
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Engine

DBBase = declarative_base()

class AppEngine:
    """LoginManager and database Engine and sessionmaker"""
    db_engine: Engine
    Session: sessionmaker
    login_manager: LoginManager
    def __init__(self, db_engine: Engine, Session: sessionmaker, login_manager: LoginManager):
        self.db_engine = db_engine
        self.Session = Session
        self.login_manager = login_manager

def initialize(app: Flask, config_data: dict[str, Any]) -> AppEngine:
    """Creates an AppEngine and creates a pointer in this module"""
    flask_env = os.environ.get("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevConfig)
    db_name = app.config["SQLALCHEMY_DATABASE_URI"]
    engine = create_engine(db_name, echo=config_data.get(dbconfig.ECHO_SQL, False))
    if config_data.get(dbconfig.DELETE_DB, False):
        DBBase.metadata.drop_all(engine)
        print('Deleting old database')
    DBBase.metadata.create_all(engine)
    login_manager = LoginManager(app)
    login_manager.login_view = "login.page"
    app_engine = AppEngine(engine, sessionmaker(engine), login_manager)
    session: Session
    with app_engine.Session() as session:
        exists = session.query(models.AboutMe).first()
        if not exists:
            about = models.AboutMe()
            session.add(about)
            session.commit()
        else:
            print('AboutMe already created')
    return app_engine

def app_engine() -> AppEngine:
    global _app_engine
    #Because modules cannot access app.py directly as it results in a circular reference,
    #it still can access the variable _app_engine when referencing inside a function
    from app import _app_engine
    return _app_engine