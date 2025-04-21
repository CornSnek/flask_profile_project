from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
import models
bp = Blueprint("login", __name__)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")

@bp.route("/login", methods=["GET", "POST"])
def page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session:Session = models.db.app_engine().Session()
        user = session.query(models.User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Logged in as user \'{current_user.username}\'', 'info')
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("dashboard.page"))
        flash('Wrong username or password.', 'error')
    return render_template("login.html", form=form)
