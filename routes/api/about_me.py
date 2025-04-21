from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from routes.dashboard import AboutMeForm
from sqlalchemy.orm import Session
import models
bp = Blueprint("about_me", __name__)

@bp.route("/about_me", methods=['POST'])
@login_required
def post():
    session: Session
    about_me_form = AboutMeForm()
    if about_me_form.validate_on_submit():
        with models.db.app_engine().Session() as session:
            try:
                about_me = session.query(models.AboutMe).get(1)
                about_me.contents = about_me_form.markdown.data
                session.commit()
            except Exception as e:
                print(e)
                flash('Unable to save','error')
        flash('Markdown saved successfully','info')
    else:
        flash('Invalid data sent', 'error')
    return redirect(url_for('dashboard.page'))