import markdown
from flask import Blueprint, render_template, request, abort, url_for
from flask_login import current_user
from sqlalchemy.orm import Session
import md_sanitizer
import requests
import models
bp = Blueprint("home", __name__)

@bp.route("/")
def page():
    session: Session
    json_responses: list[requests.Response]
    filter_lang = request.args.get('language_id', default=None, type=int)
    with models.db.app_engine().Session() as session:
        if filter_lang:
            project_ids = (
                session.query(models.Project.id)
                .join(models.ATLanguageProject)
                .where(models.ATLanguageProject.language_id==filter_lang)
                .all()
            )
        else:
            project_ids = session.query(models.Project.id).all()
        languages_db = session.query(models.Language).order_by(models.Language.name).all()
        json_responses = [requests.get(url_for('project.output', pid=project_id.id, type='html', _external=True)) for project_id in project_ids]
        about_me = session.query(models.AboutMe.contents).filter_by(id=1).one()
    projects_html = ''
    for jr in json_responses:
        if jr.status_code == 200:
            projects_html += jr.text
        else:
            abort(500)
    return render_template("home.html",
                           current_user=current_user,
                           projects_html=projects_html,
                           languages_db=languages_db,
                           filter_lang=filter_lang,
                           about_me_markdown=md_sanitizer.sanitizer.sanitize(markdown.markdown(about_me.contents))
    )