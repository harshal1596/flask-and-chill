from flask import Flask, Blueprint
from flask_restful import Api
from Resource.v1.resource import V1GetItemsResource
from Resource.v2.resource import V2GetItemsResource

app = Flask(__name__)

v1_blp = Blueprint("v1", __name__)
v2_blp = Blueprint("v2", __name__)

api_v1 = Api(v1_blp)
api_v2 = Api(v2_blp)

api_v1.add_resource(V1GetItemsResource, "/items")
api_v2.add_resource(V2GetItemsResource, "/items")

app.register_blueprint(v1_blp, url_prefix="/api/v1")
app.register_blueprint(v2_blp, url_prefix="/api/v2")

if __name__ == "__main__":
    app.run(debug=True)

