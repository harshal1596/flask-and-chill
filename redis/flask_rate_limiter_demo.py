from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per hour"]
)


@app.route('/test')
@limiter.limit('3 per hour')
def hello_world():
    return {
        "Message": "Hello world"
    }, 200


@app.route('/test1')
def hello_again():
    return {
        "Message": "Hello again"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)
