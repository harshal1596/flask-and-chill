from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "Error": e
        }), 400
    return jsonify({
        "Message": "User added"
    }), 201

@app.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "name": u.name} for u in users])

if __name__ == "__main__":
    app.run(debug=True)
