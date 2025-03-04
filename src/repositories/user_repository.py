from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schema import UserCreate

def find_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def insert_new_user(db: Session, user_create: UserCreate):
    db_user = User(name=user_create.name, email=user_create.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
