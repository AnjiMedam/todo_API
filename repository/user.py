import traceback
from fastapi import HTTPException,status
from loguru import logger
import models
import schemas
from sqlalchemy.orm import Session
from hashing import Hash
from sqlalchemy import and_

def create(request: schemas.User, db: Session):
    user_exist = db.query(models.User).filter(models.User.username == request.username).first()
    if user_exist:
        logger.warning("Username was already present..")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username was already Available")

    db_user = models.User(username=request.username, email=request.email, password=Hash.get_password_hash(request.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # if Hash.verify_password(request.password,db_user.password):
    #     print("yes, plain and hashed both are same ...")

    print(db_user.password,"------------------------------------>")
    return db_user

def get_one(id:int,db:Session):
    user_exits= db.query(models.User).filter(models.User.id == id).first()
    if not user_exits :
        logger.error(f"user was not found at {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present at {id}')
    return user_exits


def get_all(db: Session):
    all_users = db.query(models.User).all()
    if not all_users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_users


def get_info(id:int,db:Session):
    userinfo= db.query(models.User).filter(models.User.id == id).first()
    return [userinfo] if userinfo else []


# def get_all_not_deleted(db:Session):
#     all_users = db.query(models.User).filter(models.User.is_delete==False).all()
#     print(all_users,"---------------< al users")
#     if not all_users :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
#     return all_users


def partiallyupdate(userid,request,request1,current_user,db):
    try:
        logger.info(f"Request method: {request.method} - /update_user/{userid}  endpoint is called by id:{userid}")
        if current_user.role == "regular":
            updateUser = db.query(models.User).filter(and_(current_user.id == userid, models.User.id == current_user.id,models.User.is_delete == False)).first()
        elif current_user.role == "admin":
            updateUser = db.query(models.User).filter(models.User.id == userid).first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        if not updateUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or You are not authorized")
        
        updateUser.email = request1.email
        db.commit()
        db.refresh(updateUser)
        return updateUser
    except Exception as e:
        logger.error(f"An error occurred while partially updating user with id {userid}: {str(e)}  -  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error occurred")

def delete_one(id:int,db:Session):
    single_user = db.query(models.User).filter(models.User.id == id,models.User.is_delete==False).first()
    if not single_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    single_user.is_delete = True
    db.commit()
    db.refresh(single_user)
    return {'msg': f'User deleted at {id} Successfully'}


def deleted_all_users(current_user,db):
    d_users = db.query(models.User).filter(models.User.is_delete==True).all()
    if not d_users:
        logger.error("no deleted data was found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No deleted data present")
    else:
        return d_users



    
