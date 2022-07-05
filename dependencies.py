from database import SessionLocal
from redis import Redis


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis_client():
    return Redis(host="localhost", port=6379, db=0)
