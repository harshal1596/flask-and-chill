from contextlib import contextmanager
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

engine = create_engine("sqlite:///users.db", echo=False)
app = Flask(__name__)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))


Base = declarative_base()

class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True) 
    email = Column(String(120), unique=True, nullable=False) 
    name = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    with get_session() as session:
        user = User(email=data["email"], name=data["name"])
        session.add(user)
    return jsonify({"message": "User added!"})



if __name__ == "__main__":
    app.run(debug=True)
