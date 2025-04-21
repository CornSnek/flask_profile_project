from flask import Blueprint, jsonify, request
from flask_login import login_required
from sqlalchemy import case
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from routes.dashboard import LanguageCreateForm, LanguageUpdateForm
from flask_wtf.csrf import validate_csrf
bp = Blueprint("at_links", __name__)
import models

@bp.route("/project/<int:pid>/link_language/<int:lid>")
@login_required
def link_language(pid:int, lid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            lp = models.ATLanguageProject(project_id=pid, language_id=lid)
            session.add(lp)
            session.commit()
        except IntegrityError:
            session.rollback()
            return jsonify({'category': 'error', 'message': 'Project-Language link already paired'}), 409
        except Exception as e:
            session.rollback()
            return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully created'}), 201

@bp.route("/project/<int:pid>/unlink_language/<int:lid>")
@login_required
def unlink_language(pid:int, lid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            lp = session.query(models.ATLanguageProject).filter_by(project_id=pid, language_id=lid).one()
            session.delete(lp)
            session.commit()
        except:
            return jsonify({'category': 'error', 'message': 'No Project-Language link found'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully deleted'}), 200

@bp.route("/project/<int:pid>/link_url/<int:uid>")
@login_required
def link_url(pid:int, uid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            up = models.ATURLProject(project_id=pid, url_id=uid)
            session.add(up)
            session.commit()
        except IntegrityError:
            session.rollback()
            return jsonify({'category': 'error', 'message': 'Project-URL link already paired'}), 409
        except Exception as e:
            session.rollback()
            return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully created'}), 201

@bp.route("/project/<int:pid>/unlink_url/<int:uid>")
@login_required
def unlink_url(pid:int, uid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            up = session.query(models.ATURLProject).filter_by(project_id=pid, url_id=uid).one()
            session.delete(up)
            session.commit()
        except:
            return jsonify({'category': 'error', 'message': 'No Project-URL link found'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully deleted'}), 200

@bp.route("/project/<int:pid>/link_image_url/<int:iuid>")
@login_required
def link_image_url(pid:int, iuid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            iup = models.ATImageURLProject(project_id=pid, image_url_id=iuid)
            session.add(iup)
            session.commit()
        except IntegrityError:
            session.rollback()
            return jsonify({'category': 'error', 'message': 'Project-ImageURL link already paired'}), 409
        except Exception as e:
            session.rollback()
            return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully created'}), 201

@bp.route("/project/<int:pid>/unlink_image_url/<int:iuid>")
@login_required
def unlink_image_url(pid:int, iuid:int):
    session: Session
    with models.db.app_engine().Session() as session:
        try:
            iup = session.query(models.ATImageURLProject).filter_by(project_id=pid, image_url_id=iuid).one()
            session.delete(iup)
            session.commit()
        except:
            return jsonify({'category': 'error', 'message': 'No Project-ImageURL link found'}), 409
    return jsonify({'category': 'info', 'message': 'Link successfully deleted'}), 200

@bp.route("/set_order", methods=["POST"])
@login_required
def sort_order():
    session: Session
    project_id = request.args.get('project_id',type=int)
    url_ids = request.args.getlist('url_id',type=int)
    image_ids = request.args.getlist('image_id',type=int)
    if not project_id or not url_ids or not image_ids:
        return jsonify({'category': 'error', 'message': 'Missing project_id, url_id, or image_id parameters'})
    with models.db.app_engine().Session() as session:
        try:
            (
                session.query(models.ATURLProject)
                    .filter_by(project_id=project_id)
                    .filter(models.ATURLProject.url_id.in_(url_ids))
                    .update({'sort_order':case(
                        *[(models.ATURLProject.url_id == uid, so) for uid, so in {url_id: index for index, url_id in enumerate(url_ids, start=1)}.items()]
                    )})
            )
            (
                session.query(models.ATImageURLProject)
                    .filter_by(project_id=project_id)
                    .filter(models.ATImageURLProject.image_url_id.in_(image_ids))
                    .update({'sort_order':case(
                        *[(models.ATImageURLProject.image_url_id == iuid, so) for iuid, so in {image_id: index for index, image_id in enumerate(image_ids, start=1)}.items()]
                    )})
            )
            session.commit()
        except Exception as e:
            session.rollback()
            return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'})
    return jsonify({'category':'info', 'message':'Ordering saved'})