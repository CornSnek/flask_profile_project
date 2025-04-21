from flask import Blueprint, jsonify, get_flashed_messages
from flask_login import login_required
bp = Blueprint("flash", __name__)

@bp.route("/flash")
def page():
    return jsonify({'messages': get_flashed_messages(with_categories=True)})