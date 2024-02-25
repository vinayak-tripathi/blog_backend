
from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from fastapi import HTTPException, status

def create(request: schemas.User,db:Session):
    new_user = models.User(name = request.name,
                           email = request.email,
                           password = hashing.Hash.encrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'User with id {id} not found')
    return db_user

def show_email(email: str, db: Session):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'User with id {id} not found')
    return db_user