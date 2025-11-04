from flask import Blueprint
from flask_restful import Api
from Resource.v1.resource import V1GetItemsResource
from Resource.v2.resource import V2GetItemsResource

VERSIONS = {
    "v1": {
        "prefix": "/api/v1",
        "deprecated": True,
        "resources": [(V1GetItemsResource, "/items")]
    },
    "v2": {
        "prefix": "/api/v2",
        "deprecated": False,
        "resources": [(V2GetItemsResource, "/items")]
    }
}

DEFAULT_VERSION = "v2"

def register_versions(app):
    for version, details in VERSIONS.items():
        if details.get('deprecated'):
            print(f"Warning: API version {version} is deprecated.")
        blp = Blueprint(f"api_{version}", __name__)
        api = Api(blp)

        for resource, url in details['resources']:
            api.add_resource(resource, url)
        app.register_blueprint(blp, url_prefix=details['prefix'])

