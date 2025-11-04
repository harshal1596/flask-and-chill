from flask import Flask
from flasgger import Swagger
from Resource.v2.resource import V2GetItemsResource
from versions import register_versions, DEFAULT_VERSION

app = Flask(__name__)
register_versions(app)

# Swagger Configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Versioned Flask API",
    "description": "This API supports multiple versions using Flask-RESTful and Blueprints.",
        "version": "1.0.0",
        "contact": {"name": "API Team", "email": "api@example.com"},
    },
    "schemes": ["http", "https"],
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # include all endpoints
            "model_filter": lambda tag: True,  # include all models
        }
    ],
    "swagger_ui": True,
    "specs_route": "/docs/",
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Optional: Default version route
@app.route("/api/users")
def default_users():
    """Get default API version response"""
    return V2GetItemsResource().get()

if __name__ == "__main__":
    app.run(debug=True)

