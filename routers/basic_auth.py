from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import get_db
import secrets
from fastapi import FastAPI
from sqlalchemy.orm import Session
import models
from hashing import Hash

security = HTTPBasic()
def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)] ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    password_hashed= Hash.get_password_hash(credentials.password)
    is_correct_password = Hash.verify_password(
        credentials.password, password_hashed
    )

    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


