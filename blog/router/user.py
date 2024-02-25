

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..repository import user
from ..database import get_db


router = APIRouter(
          prefix = "/user",
          tags=['Users']
          )

@router.post("/", 
             response_model=schemas.ShowUser)
def create_user(user_object: schemas.User,
                db: Session = Depends(get_db)):
    
    return user.create(user_object, db)

@router.get("/{id}", 
            response_model=schemas.ShowUser)
def get_user(id: int,
             db: Session = Depends(get_db)):
    return user.show(id, db)