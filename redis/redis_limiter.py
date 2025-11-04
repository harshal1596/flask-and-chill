from typing import Iterable, Optional
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

"""
redis_limiter.py

Helper to wire Redis as the storage backend for Flask-Limiter.
Creates and returns a Limiter configured to use Redis, and shows a tiny example route.
"""




def init_redis_limiter(
    app: Flask,
    redis_url: str = "redis://127.0.0.1:6379/0",
    default_limits: Optional[Iterable[str]] = None,
    key_func=get_remote_address,
) -> Limiter:
    """
    Initialize and attach a Flask-Limiter to a Flask app using Redis as storage.

    Parameters:
    - app: Flask application instance
    - redis_url: Redis URI (e.g. "redis://localhost:6379/0")
    - default_limits: iterable of rate strings (e.g. ["100/hour", "10/minute"])
    - key_func: function to extract the rate-limiting key (defaults to remote address)

    Returns:
    - Limiter instance
    """
    if default_limits is None:
        default_limits = ["200 per day", "50 per hour"]

    limiter = Limiter(
        app,
        key_func=key_func,
        default_limits=list(default_limits),
        storage_uri=redis_url,
    )
    return limiter


# Example usage when running this file directly
if __name__ == "__main__":
    app = Flask(__name__)

    # configure limiter using Redis at the default URL
    limiter = init_redis_limiter(app, redis_url="redis://127.0.0.1:6379/1")

    @app.route("/ping")
    @limiter.limit("10/minute")  # route-specific override using Redis-backed storage
    def ping():
        return jsonify({"pong": True})

    @app.route("/info")
    def info():
        # uses default limits configured above
        return jsonify({"limits": limiter._defaults})  # simple introspection

    app.run(host="0.0.0.0", port=5000, debug=True)