

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, hashing
from ..database import get_db


router = APIRouter()

@router.post("/user", 
          response_model=schemas.ShowUser,
          tags=['User'])
def create_user(user: schemas.User,
                db: Session = Depends(get_db)):
    
    new_user = models.User(name = user.name,
                           email = user.email,
                           password = hashing.Hash.encrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}", 
          response_model=schemas.ShowUser,
          tags=['User'])
def get_user(id: int,
             db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'User with id {id} not found')
    
    return db_user