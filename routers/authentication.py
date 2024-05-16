from datetime import datetime, timedelta, timezone
import traceback
from fastapi import APIRouter, Depends, Request, status, HTTPException
from typing import List
from fastapi import security
from jose import ExpiredSignatureError, JWTError,jwt
from loguru import logger
import database
import models
from sqlalchemy.orm import Session
from routers.basic_auth import get_current_username
import schemas
from hashing import Hash
import JWTtoken 
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

@router.post("/basic_auth",status_code=status.HTTP_201_CREATED)
def login(user: models.User = Depends(get_current_username)):
    return {"message": f"Login successful by user:{user.username}"}


@router.post("/login",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],request:Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request method: {request.method} - /login API endpoint called by user:{form_data.username}")
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
    
    except Exception as e:
        logger.error(f"request_method : {request.method} - /login/  error -{e}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/login/refresh")
def refresh_access_token(refresh_token:str,request:Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request method: {request.method} - /login/refresh/ -API endpoint called ")
        payload = jwt.decode(refresh_token, JWTtoken.SECRET_KEY, algorithms=[JWTtoken.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.info(f'at {request.method} -invalid token error..')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        expiration_time = payload.get("exp")
        if expiration_time is not None:
            current_time = datetime.now(timezone.utc).timestamp()
            if current_time >= expiration_time:
                logger.info("you have to change the refresh expires time ")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired")

        access_token = JWTtoken.create_access_token(data={"sub": username})   

        data={"access_token": access_token,'username':f'{username}', "token_type": "bearer"}
        logger.info(data)
        # schemas.Token(access_token=access_token,refresh_token=refresh_token, token_type="bearer")
        return {"access_token": access_token,'username':f'{username}', "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        logger.error(f"request_method : {request.method} - /login/refresh/  error -{e}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



