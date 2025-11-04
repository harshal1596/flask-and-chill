from flask import Blueprint, jsonify

v2_blueprint = Blueprint("v2", __name__, url_prefix="/api/v2")

@v2_blueprint.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": ["item1", "item2", "item3", "item4"]})
