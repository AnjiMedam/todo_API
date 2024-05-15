from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from jose import ExpiredSignatureError, JWTError,jwt
from loguru import logger
import database
import models
from sqlalchemy.orm import Session
import schemas
from hashing import Hash
import JWTtoken 
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db
 
@router.post("/login",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    # logger.info("form data is %s",form_data)
    print(form_data)
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user:
        logger.warning("Incorrect credential AT username not matching..!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect credentials")

    if not Hash.verify_password(form_data.password,user.password):
        logger.warning("Incorrect password...")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Password")
     
    access_token = JWTtoken.create_access_token(data={"sub": user.username})
    refresh_token = JWTtoken.create_refresh_token(data={"sub": user.username})
 
    print("printing access_token which is generated: ", access_token)
    print("printing refresh_token which is generated: ", refresh_token)
    return schemas.Token(access_token=access_token,refresh_token=refresh_token, token_type="bearer")

@router.post("/login/refresh")
def refresh_access_token(refresh_token:str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, JWTtoken.SECRET_KEY, algorithms=[JWTtoken.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        expiration_time = payload.get("exp")
        if expiration_time is not None:
            current_time = datetime.now(timezone.utc).timestamp()
            if current_time >= expiration_time:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired")

        access_token = JWTtoken.create_access_token(data={"sub": username})   

        return {"access_token": access_token,'username':f'{username}', "token_type": "bearer"}

    # except ExpiredSignatureError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")





