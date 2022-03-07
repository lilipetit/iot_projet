from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_students(db: Session):
    return db.query(models.User).where(models.User.role_id == 3).all()


def create_user(db: Session, email: str, password: str, role_id: int):
    db_user = models.User(email=email, hashed_password=password, role_id=role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
