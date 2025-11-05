import time
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from flask import Flask, request, jsonify, g

client = MongoClient(f"mongodb://localhost:27017/")
db = client["myapp"]
users = db["users"]

app = Flask(__name__)

@app.before_request
def start_session():
    g.session = client.start_session()

@app.teardown_request
def teardown_session():
    if hasattr(g, "session"):
        g.session.end_session()

@app.request("/transaction", methods=['POST'])
def add_transactions():
    try:
        with g.session.start_transaction():
            db.users.update_one(..., session=g.session)
            db.logs.insert_one(..., session=g.session)
        return {"message": "ok"}
    except:
        return {"message": "failed"}, 400
    # in case you want to retry on failure
    # except PyMongoError as e:
    #     time.sleep(0.5) 
