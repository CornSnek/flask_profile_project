from flask import Flask
from typing import Any
from sqlalchemy.orm import Session
import json

config_data: dict[str, Any]
with open("config.json") as cf:
    config_data = json.load(cf)

app = Flask(__name__)

import models
_app_engine: models.db.AppEngine = models.db.initialize(app, config_data)
""" Use models.db.app_engine() as a pointer to this as other modules cannot access app.py due to circular reference """

@_app_engine.login_manager.user_loader
def load_user(user_id):
    session: Session
    with _app_engine.Session() as session:
        user = session.query(models.User).filter_by(id=user_id).first()
    return user

import routes
app.register_blueprint(routes.home.bp)
app.register_blueprint(routes.login.bp)
app.register_blueprint(routes.dashboard.bp, url_prefix="/dashboard")
app.register_blueprint(routes.api.flash.bp, url_prefix="/api")
app.register_blueprint(routes.api.about_me.bp, url_prefix="/api")
app.register_blueprint(routes.api.languages.bp, url_prefix="/api")
app.register_blueprint(routes.api.urls.bp, url_prefix="/api")
app.register_blueprint(routes.api.image_urls.bp, url_prefix="/api")
app.register_blueprint(routes.api.project.bp, url_prefix="/api")
app.register_blueprint(routes.api.at_links.bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)