from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
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

@router.post("/login/",status_code=status.HTTP_201_CREATED)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    
    print(form_data)
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    print("user----------------->",user.username)
    
    if not user:
        print(" i am  not user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect credentials")

    if not Hash.verify_password(form_data.password,user.password):
        print(" i am in verfy passwod")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Password")
    

    access_token = JWTtoken.create_access_token(
        data={"sub": user.username})
    
    # here username or admin is anji
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # c_user= JWTtoken.verify_token(access_token,credentials_exception,db)
    # if(c_user == user.username):
    #     print("user from token and admin user both were same...")

    print("print access_token generated: ", access_token)
    return schemas.Token(access_token=access_token, token_type="bearer")


