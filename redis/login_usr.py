from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

app = Flask(__name__)

# --- Config ---
app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"  # Use env var in production!
app.config["RATELIMIT_STORAGE_URI"] = "redis://localhost:6379"

# --- Setup Redis client ---
redis_client = redis.Redis(host='localhost', port=6378, db=0, decode_responses=True)

# --- Initialize JWT & Limiter ---
jwt = JWTManager(app)

# key_func -> determines "who" is being limited (user_id from JWT, else IP)
def user_rate_limit_key():
    if request.path.startswith("/login"):
        # For login, use IP-based limiting to prevent brute-force
        return get_remote_address()
    try:
        return get_jwt_identity() or get_remote_address()
    except Exception:
        return get_remote_address()

limiter = Limiter(
    key_func=user_rate_limit_key,
    app=app,
    default_limits=["200 per hour"],  # global default
    storage_uri="redis://localhost:6378"
)


# --- Example user store (for demo only) ---
USERS = {
    "alice": "password123",
    "bob": "securepass"
}


# --- Login endpoint (IP-based rate limit) ---
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")  # protects against brute-force attacks
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in USERS or USERS[username] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify(access_token=token)


# --- Protected API endpoint (JWT-based rate limit) ---
@app.route("/api/profile")
@jwt_required()
@limiter.limit("20 per minute")  # applies per authenticated user
def profile():
    user = get_jwt_identity()
    return jsonify({
        "user": user,
        "profile": f"Profile data for {user}"
    })


# --- Another example endpoint with different limits ---
@app.route("/api/data")
@jwt_required()
@limiter.limit("100 per hour; 10 per minute")  # layered limits
def get_data():
    user = get_jwt_identity()
    return jsonify({
        "user": user,
        "data": "This is user-specific data"
    })


# --- Error handler for rate limiting ---
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({
        "error": "rate_limit_exceeded",
        "message": str(e.description)
    }), 429


if __name__ == "__main__":
    app.run(debug=True)
