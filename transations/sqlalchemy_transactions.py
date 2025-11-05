from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

app = Flask(__name__)
engine = create_engine("sqlite:///users.db", echo=False)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)

Base.metadata.create_all(engine)

def transfer_money(from_user_id, to_user_id, amount):
    session = SessionLocal()
    try:
        sender = session.User.query(name=from_user_id)
        receiver = session.User.query(name=to_user_id)

        if sender.balance < amount:
            raise ValueError("Insufficient balance")
        
        sender.balance -= amount
        receiver.balance += amount

        session.commit()  # Commit if all succeeded
        print("Transaction committed")
    
    except Exception as e:
        session.rollback()  # Rollback on any error
        print("Transaction rolled back:", e)

    finally:
        session.close()
    