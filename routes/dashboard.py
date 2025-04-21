from flask import Blueprint, redirect, url_for, render_template, flash, abort, request
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, HiddenField
from wtforms.validators import Length, InputRequired, URL, ValidationError
from sqlalchemy.orm import Session
import requests
import models
import md_sanitizer
import markdown

class AboutMeForm(FlaskForm):
    markdown = TextAreaField('Markdown', validators=[Length(max=2000)], render_kw={"class": "textarea-edit"})
    submit = SubmitField('Submit')

bp = Blueprint("dashboard", __name__)

@bp.route("/")
@login_required
def page():
    about_me_form = AboutMeForm()
    session: Session
    with models.db.app_engine().Session() as session:
        languages_db = session.query(models.Language).order_by(models.Language.name).all()
        projects_db = session.query(models.Project.id, models.Project.name).order_by(models.Project.name).all()
        urls_db = session.query(models.URL).order_by(models.URL.name).all()
        image_urls_db = session.query(models.ImageURL).order_by(models.ImageURL.name).all()
        about_me_db = session.query(models.AboutMe.contents).filter_by(id=1).one()
    about_me_form.markdown.data = about_me_db.contents
    return render_template('dashboard.html',
                           current_user=current_user,
                           about_me_form=about_me_form,
                           about_me_html=md_sanitizer.sanitizer.sanitize(markdown.markdown(about_me_db.contents)),
                           languages_db=languages_db,
                           projects_db=projects_db,
                           urls_db=urls_db,
                           image_urls_db=image_urls_db
    )

class LanguageCreateForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')

class LanguageUpdateForm(LanguageCreateForm):
    id = HiddenField('ID')

@bp.route("/language/create")
@login_required
def language_create():
    form = LanguageCreateForm()
    return render_template('dashboard/create_language.html', form=form)

@bp.route("/language/<int:lid>")
@login_required
def language_update(lid:int):
    form = LanguageUpdateForm()
    session: Session
    with models.db.app_engine().Session() as session:
        language = session.query(models.Language).filter_by(id=lid).one()
        form.name.data=language.name
        form.id.data=lid
        used_in_projects = session.query(models.Project.id, models.Project.name).filter(models.Project.id.in_(
            session.query(models.ATLanguageProject.project_id).filter_by(language_id=lid)
        )).all()
        not_used_in_projects = session.query(models.Project.id, models.Project.name).filter(~models.Project.id.in_(
            session.query(models.ATLanguageProject.project_id).filter_by(language_id=lid)
        )).all()
    return render_template('dashboard/update_language.html',
                           form=form,
                           used_in_projects=used_in_projects,
                           not_used_in_projects=not_used_in_projects
    )

class URLCreateForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    url = StringField('URL', validators=[InputRequired(), 
                                         URL(allow_ip=False, 
                                             message='Invalid URL (IPs are forbidden and top-level domains are required).'
                                             )])
    description = StringField('Description', validators=[InputRequired()])
    submit = SubmitField('Submit')

class URLUpdateForm(URLCreateForm):
    id = HiddenField('ID')

@bp.route("/url/create")
@login_required
def url_create():
    form = URLCreateForm()
    return render_template('dashboard/create_url.html', form=form)

@bp.route("/url/<int:uid>")
@login_required
def url_update(uid:int):
    form = URLUpdateForm()
    session: Session
    with models.db.app_engine().Session() as session:
        url = session.query(models.URL).filter_by(id=uid).one()
        form.name.data=url.name
        form.url.data=url.url
        form.description.data=url.description
        form.id.data=url.id
        used_in_projects = session.query(models.Project.id, models.Project.name).filter(models.Project.id.in_(
            session.query(models.ATURLProject.project_id).filter_by(url_id=uid)
        )).all()
        not_used_in_projects = session.query(models.Project.id, models.Project.name).filter(~models.Project.id.in_(
            session.query(models.ATURLProject.project_id).filter_by(url_id=uid)
        )).all()
    return render_template('dashboard/update_url.html', 
                           form=form, 
                           used_in_projects=used_in_projects,
                           not_used_in_projects=not_used_in_projects
    )

def is_image_url(_, field):
    try:
        response = requests.head(field.data, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("image/"):
            raise ValidationError('The URL should link to a valid image.')
    except requests.RequestException:
        raise ValidationError('Unable to verify the image URL.')

class ImageURLCreateForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    url = StringField('URL', validators=[InputRequired(), URL(allow_ip=False, 
                                                              message='Invalid URL (IPs are forbidden and top-level domains are required).'), 
                                                              is_image_url]
                                                              )
    description = StringField('Description', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ImageURLUpdateForm(ImageURLCreateForm):
    id = HiddenField('ID')

@bp.route("/image_url/create")
@login_required
def image_url_create():
    form = ImageURLCreateForm()
    return render_template('dashboard/create_image_url.html', form=form)

@bp.route("/image_url/<int:iuid>")
@login_required
def image_url_update(iuid:int):
    form = ImageURLUpdateForm()
    session: Session
    with models.db.app_engine().Session() as session:
        url = session.query(models.ImageURL).filter_by(id=iuid).one()
        form.name.data=url.name
        form.url.data=url.url
        form.description.data=url.description
        form.id.data=url.id
        used_in_projects = session.query(models.Project.id, models.Project.name).filter(models.Project.id.in_(
            session.query(models.ATImageURLProject.project_id).filter_by(image_url_id=iuid)
        )).all()
        not_used_in_projects = session.query(models.Project.id, models.Project.name).filter(~models.Project.id.in_(
            session.query(models.ATImageURLProject.project_id).filter_by(image_url_id=iuid)
        )).all()
    return render_template('dashboard/update_image_url.html', 
                           form=form, 
                           used_in_projects=used_in_projects,
                           not_used_in_projects=not_used_in_projects
    )

class ProjectCreateForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()], render_kw={"class": "textarea-edit"})
    submit = SubmitField('Submit')

class ProjectUpdateForm(ProjectCreateForm):
    id = HiddenField('ID')

@bp.route("/project/create")
@login_required
def project_create():
    form = ProjectCreateForm()
    return render_template('dashboard/create_project.html', form=form)

@bp.route("/project/<int:pid>")
@login_required
def project_update(pid:int):
    form = ProjectUpdateForm()
    #Using requests doesn't send the session cookie normally
    cookies = {'session': request.cookies.get('session')}
    project_resp_html = requests.get(url_for('project.output', pid=pid, type='html_edit', _external=True), cookies=cookies)
    project_resp_json = requests.get(url_for('project.output', pid=pid, type='json', _external=True))
    if project_resp_html.status_code == 200 and project_resp_json.status_code == 200:
        project_html=project_resp_html.text
        project_json=project_resp_json.json()
    else:
        abort(500)
    form.name.data = project_json['name']
    form.content.data = project_json['content']
    form.id.data = pid
    return render_template('dashboard/update_project.html', 
                           form=form,
                           project_html=project_html, 
                           project_json=project_json)

@bp.route("/logout")
@login_required
def logout():
    flash(f'Logged out user \'{current_user.username}\'', 'info')
    logout_user()
    return redirect(url_for('home.page'))