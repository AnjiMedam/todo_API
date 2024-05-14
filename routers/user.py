from typing import List,Annotated
from fastapi import APIRouter, Depends, Request, status, HTTPException
from loguru import logger
import schemas, database, models
from sqlalchemy.orm import Session
import schemas
import database
from repository import user
from oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db

@router.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)


@router.get("/get_user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def get_user(current_user: Annotated[schemas.User, Depends(get_current_user)],id:int ,db: Session = Depends(get_db)):
    
    if current_user.role == "admin":
        return user.get_one(id,db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})
    

@router.get("/get_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUserWithId])
def get_users(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):

    if current_user.role == "admin":
        return user.get_all(db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Only admins are able to authorize")


@router.get("/get_myinfo/",status_code=status.HTTP_200_OK,response_model=List[schemas.Userwithoutpass])
def get_myinfo(current_user: Annotated[schemas.User, Depends(get_current_user)],db:Session = Depends(get_db)):
    logger.info("Getting info of users...")
    if current_user.role in 'admin':
        return user.get_info(current_user.id,db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})


@router.patch("/update_user/{userid}",status_code=status.HTTP_201_CREATED,response_model=schemas.UserBase)
def update_user(request:Request,current_user: Annotated[schemas.User, Depends(get_current_user)],userid:int,request1: schemas.UserBase, db: Session = Depends(get_db)):

    return user.partiallyupdate(userid,request,request1,current_user,db)


@router.delete("/delete_user/{id}",status_code=status.HTTP_200_OK)
def delete_user(current_user: Annotated[schemas.User, Depends(get_current_user)],id:int,db:Session= Depends(get_db)):

    if current_user.role == "admin":
        return user.delete_one(id,db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})
    

@router.get("/deleted_users",response_model=List[schemas.ShowUserwithDeleteFlag] )
def deleted_user(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):

    if not current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail={'msg':"Only admins are able to authorize"})
    else:
        return user.deleted_all_users(current_user,db)
    
        