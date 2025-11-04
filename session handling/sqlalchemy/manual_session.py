from flask import Flask, g, jsonify, request
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

app = Flask(__name__)
engine = create_engine("sqlite:///users.db", echo=False)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

Base = declarative_base()

class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True) 
    email = Column(String(120), unique=True, nullable=False) 
    name = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

@app.before_request
def create_tables():
    g.db = SessionLocal()           # Create tables

@app.teardown_request
def close_session(exception=None):
    db = getattr(g, "db", None) 
    if db is not None: 
        if exception: 
            db.rollback() 
        db.close()

@app.route("/getUsers")
def get_users():
    users = g.db.query(User).all()
    return jsonify([{"id": u.id, "email": u.email, "name": u.name} for u in users])


@app.route("/addUser", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(email=data["email"], name=data["name"])
    g.db.add(new_user)
    try:
        g.db.commit()
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 400 
    return jsonify({"message": "User added!"}), 201 

if __name__ == "__main__":
    app.run(debug=True)

