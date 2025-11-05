from pymongo import MongoClient
from flask import Flask, request, jsonify

client = MongoClient(f"mongodb://localhost:27017/")
db = client["myapp"]
users = db["users"]

app = Flask(__name__)


@app.route("/GetUsers")
def get_users():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    skip = (page-1) * per_page

    count_users = users.count_documents({})
    users_data = users.find().skip(skip).limit(per_page)

    data = list(users_data)
    for u in data:
        u["_id"] = str(u["_id"])

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": count_users,
        "total_pages": (count_users + per_page - 1) // per_page,
        "data": data
    })
    
# Above solution is better in case of small number of documents. In case of skipping 1000000 documents 
# above solution is not suitable

# Cursor-based pagination (also called “range-based”) uses a unique, 
# indexed field (like _id or created_at) to fetch the next set of documents efficiently.
from bson import ObjectId

@app.route("users_cursor", methods=["GET"])
def get_users_cursor():
    per_page = int(request.args.get("per_page", 5))
    last_id = request.args.get("last_id")

    query = {}
    if last_id:
        query['last_id'] = {
            "$gt": ObjectId(last_id)        # fetch newer records greater than id mentioned
        }

    docs = users.find(query).sort("_id", 1).limit(per_page)
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    
    next_cursor = docs[-1]["_id"] if docs else None         # last id for fetching next records

    return jsonify({
        "data": docs,
        "next_cursor": next_cursor
    })


# Query example with pagination
# query = {
#     "name": {
#         "$regex": name,
#         "$options": "i"         # makes case-insensitive
#     }
# }
# users.find(query).skip(skip).limit(limit)
