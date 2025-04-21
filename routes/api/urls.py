from flask import Blueprint, redirect, url_for, flash, abort, jsonify
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from routes.dashboard import URLCreateForm, URLUpdateForm
from flask_wtf.csrf import validate_csrf
bp = Blueprint("urls", __name__)
import models

@bp.route("/urls/create", methods=['POST'])
@login_required
def create():
    form = URLCreateForm()
    session: Session
    if form.validate_on_submit():
        with models.db.app_engine().Session() as session:
            name = form.name.data
            url = form.url.data
            description = form.description.data
            try:
                new_item = models.URL(name=name, url=url, description=description)
                session.add(new_item)
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate Name used: \'{name}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'URL successfully created: \'{name}\''}), 201
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400
    
@bp.route("/urls/update", methods=['POST'])
@login_required
def update():
    form = URLUpdateForm()
    if form.validate_on_submit():
        session: Session
        with models.db.app_engine().Session() as session:
            try:
                url = session.query(models.URL).get(form.id.data)
                url.name = form.name.data
                url.url = form.url.data
                url.description = form.description.data
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Duplicate name used: \'{form.name.data}\''}), 409
            except Exception as e:
                session.rollback()
                return jsonify({'category': 'error', 'message': f'Unexpected error: {e}'}), 409
        return jsonify({'category': 'info', 'message': f'URL successfully updated'})
    else:
        return jsonify({'category': 'error', 'message': 'Form submit invalid', 'wtferrors': form.errors}), 400
    
@bp.route("/urls/delete", methods=['POST'])
@login_required
def delete():
    form = URLUpdateForm()
    session: Session
    try:
        validate_csrf(form.csrf_token.data)
    except:
        flash(f'Form submit invalid', 'error')
        return redirect(url_for('dashboard.page'))
    with models.db.app_engine().Session() as session:
        url = session.query(models.URL).get(form.id.data)
        if not url:
            flash(f'Unknown id deletion', 'error')
            return redirect(url_for('dashboard.page'))
        try:
            session.delete(url)
            session.commit()
            flash(f'URL \'{url.name}\' successfully deleted', 'info')
        except Exception as e:
            session.rollback()
            flash(f'Unexpected error: {e}', 'error')
            return redirect(url_for('dashboard.page'))
    return redirect(url_for('dashboard.page'))
        