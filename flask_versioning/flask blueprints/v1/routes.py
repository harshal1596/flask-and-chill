from flask import Blueprint, jsonify

v1_blueprint = Blueprint("v1", __name__, url_prefix="/api/v1")

@v1_blueprint.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": ["item1", "item2", "item3"]})
