from flask import Blueprint, jsonify, request, abort, render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from routes.dashboard import ProjectCreateForm, ProjectUpdateForm
from flask_wtf.csrf import validate_csrf
import models
import md_sanitizer
import markdown
bp = Blueprint("project", __name__)

@bp.route("/project/<int:pid>")
def output(pid:int):
    return_type = request.args.get('type', default='json')
    if return_type not in ['json','html','html_edit']:
        abort(400)
    if return_type == 'html_edit':
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
    session: Session
    json_return = {}
    response: int
    with models.db.app_engine().Session() as session:
        project = session.query(models.Project).filter_by(id=pid).first()
        if project:
            languages = session.query(models.Language).filter(models.Language.id.in_(
                session.query(models.ATLanguageProject.language_id).filter_by(project_id=pid)
            )).all()
            urls = session.query(models.URL).join(models.ATURLProject).where(models.ATURLProject.project_id==pid).order_by(models.ATURLProject.sort_order).all()
            image_urls = session.query(models.ImageURL).join(models.ATImageURLProject).where(models.ATImageURLProject.project_id==pid).order_by(models.ATImageURLProject.sort_order).all()
            json_return['id'] = project.id
            json_return['name'] = project.name
            json_return['content'] = project.content
            json_return['languages'] = [{'id':language.id, 'name':language.name} for language in languages]
            json_return['urls'] = [{'name':url.name, 'id':url.id, 'url':url.url, 'description':url.description} for url in urls]
            json_return['image_urls'] = [{'name':image_url.name, 'id':image_url.id, 'url':image_url.url, 'description':image_url.description} for image_url in image_urls]
            response = 200
        else:
            json_return['error'] = f'Invalid id={pid}'
            response = 400
    if return_type=='json':
        return jsonify(json_return), response
    else:
        if response != 400:
            json_return['content']=md_sanitizer.sanitizer.sanitize(markdown.markdown(json_return['content']))
            return render_template('macros/impl/' + ('project.html' if return_type=='html' else 'project_edit.html'),project_json=json_return)
        else:
            return f'{json_return}', 400

@bp.route("/project/create", methods=['POST'])
@login_required
def create():
    form = ProjectCreateForm()
    session: Session
    if form.validate_on_submit():
        with models.db.app_engine().Session() as session:
            name = form.name.data
            content = form.content.data
            try:
                new_item = models.Project(name=name, content=content)
                session.add(new_item)
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate Name used: \'{name}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'Project successfully created: \'{name}\''}), 201
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400

@bp.route("/project/update", methods=['POST'])
@login_required
def update():
    form = ProjectUpdateForm()
    if form.validate_on_submit():
        session: Session
        with models.db.app_engine().Session() as session:
            try:
                project = session.query(models.Project).get(form.id.data)
                project.name = form.name.data
                project.content = form.content.data
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate name used: \'{form.name.data}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'Project successfully updated'})
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400

@bp.route("/project/delete", methods=['POST'])
@login_required
def delete():
    form = ProjectUpdateForm()
    session: Session
    try:
        validate_csrf(form.csrf_token.data)
    except:
        flash(f'Form submit invalid', 'error')
        return redirect(url_for('dashboard.page'))
    with models.db.app_engine().Session() as session:
        project = session.query(models.Project).get(form.id.data)
        if not project:
            flash(f'Unknown id deletion', 'error')
            return redirect(url_for('dashboard.page'))
        try:
            session.delete(project)
            session.commit()
            flash(f'Project \'{project.name}\' successfully deleted', 'info')
        except Exception as e:
            session.rollback()
            flash(f'Unexpected error: {e}', 'error')
            return redirect(url_for('dashboard.page'))
    return redirect(url_for('dashboard.page'))

