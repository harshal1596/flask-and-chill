from flask import Flask, request, jsonify, g
from pymongo import MongoClient
from pymongo.errors import PyMongoError 

client = MongoClient(f"mongodb://localhost:27017/")
db = client["myapp"]
users = db["users"]

app = Flask(__name__)

@app.before_request
def create_session():
    g.session = client.start_session()

@app.teardown_request
def end_session():
    session = getattr(g, "session", None)
    if session:
        session.end_session()


@app.route("/transation", methods=["POST"])
def add_transations():
    data = request.get_json()
    from_email = data["from"]
    to_email = data["to"]
    amount = data["amount"]
    session = g.session 
    try:
        with g.session.start_transaction():
            users.update_one({"email": from_email},
                {"$inc": {"balance": -amount}},
                session=session
            )

            users.update_one(
                {"email": to_email},
                {"$inc": {"balance": amount}},
                session=session
            )
            return jsonify({"message": "Transfer successful"}), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 400
    

