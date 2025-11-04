from flask import Flask
from v1.routes import v1_blueprint
from v2.routes import v2_blueprint

app = Flask(__name__)
app.register_blueprint(v1_blueprint, url_prefix="/api/v1")
app.register_blueprint(v2_blueprint, url_prefix="/api/v2")

if __name__ == "__main__":
    app.run(debug=True)

