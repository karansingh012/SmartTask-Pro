from flask import Blueprint, jsonify


analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="ok")
