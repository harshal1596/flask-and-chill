from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError 

client = MongoClient(f"mongodb://localhost:27017/")
db = client["myapp"]
users = db["users"]
app = Flask(__name__)

@app.route("/transaction", methods=["POST"])
def add_users_data():
    data = request.get_json()
    with client.start_session() as session:
        try:
            with session.start_transaction():
                users.insert_one({"email": data["email"], "balance": 100}, session=session)
                db["logs"].insert_one({"event": "user_created", "email": data["email"]}, session=session)
            
            return jsonify({
                "Message": "Data inserted successfully"
            }), 201
        
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
