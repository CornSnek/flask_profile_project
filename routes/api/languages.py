from flask import Blueprint, redirect, url_for, flash, abort, jsonify
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from routes.dashboard import LanguageCreateForm, LanguageUpdateForm
from flask_wtf.csrf import validate_csrf
bp = Blueprint("languages", __name__)
import models

@bp.route("/languages/create", methods=['POST'])
@login_required
def create():
    form = LanguageCreateForm()
    if form.validate_on_submit():
        name = form.name.data
        session: Session
        with models.db.app_engine().Session() as session:
            try:
                new_item = models.Language(name=name)
                session.add(new_item)
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate Name used: \'{name}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'Language/Tag successfully created: \'{name}\''}), 201
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400

@bp.route("/languages/update", methods=['POST'])
@login_required
def update():
    form = LanguageUpdateForm()
    if form.validate_on_submit():
        name = form.name.data
        session: Session
        with models.db.app_engine().Session() as session:
            try:
                language = session.query(models.Language).get(form.id.data)
                old_name = language.name
                language.name = name
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate name used: \'{name}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'Language/Tag successfully updated from \'{old_name}\' to \'{name}\''})
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400

@bp.route("/languages/delete", methods=['POST'])
@login_required
def delete():
    form = LanguageUpdateForm()
    session: Session
    try:
        validate_csrf(form.csrf_token.data)
    except:
        flash(f'Form submit invalid', 'error')
        return redirect(url_for('dashboard.page'))
    with models.db.app_engine().Session() as session:
        language = session.query(models.Language).get(form.id.data)
        if not language:
            flash(f'Unknown id deletion', 'error')
            return redirect(url_for('dashboard.page'))
        try:
            session.delete(language)
            session.commit()
            flash(f'Language/Tag \'{language.name}\' successfully deleted', 'info')
        except Exception as e:
            session.rollback()
            flash(f'Unexpected error: {e}', 'error')
            return redirect(url_for('dashboard.page'))
    return redirect(url_for('dashboard.page'))