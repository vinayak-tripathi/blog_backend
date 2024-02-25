from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db

from . import token
from .repository import user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

async def get_current_user(token_str: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    verified_token = token.verify(token_str, credentials_exception)
    # user = get_user(fake_users_db, username=token_data.username)
    user_object = user.show_email(verified_token.email, db)
    # if user is None:
    #     raise credentials_exception
    return user_object
