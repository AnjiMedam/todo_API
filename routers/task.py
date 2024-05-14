from typing import List,Annotated
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
import schemas
import database
from repository import task
from oauth2 import get_current_user

router = APIRouter(
    prefix="/task",
    tags=['Tasks']
)

get_db = database.get_db

@router.post("/create_task/",status_code=status.HTTP_201_CREATED,response_model=schemas.TaskBase)
def create_task(current_user: Annotated[schemas.User, Depends(get_current_user)],request:schemas.TaskBase,db:Session = Depends(get_db)):
    print("current_user--------------->",current_user)
    return task.add_task(request,db,current_user)


@router.get("/get_task/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowTask)
def get_task(current_user: Annotated[schemas.User, Depends(get_current_user)],id:int,db:Session = Depends(get_db)):
    if current_user.role == "admin":
        return task.get_one(id,db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})
        

@router.get("/get_tasks/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowTask])
def get_tasks(current_user: Annotated[schemas.User, Depends(get_current_user)],db: Session = Depends(get_db)):
    if current_user.role == "admin":
        return task.get_all(db)
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})


@router.get("/get_cuser_tasks/",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def get_cuser_tasks(current_user: Annotated[schemas.User, Depends(get_current_user)],db:Session = Depends(get_db)):
    if current_user.role in ('admin','regular'):
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail= {"msg":"Only admins are able to authorize"})


@router.put("/update_task/{taskid}",status_code=status.HTTP_201_CREATED,response_model=schemas.TaskBase)
def update_task(current_user: Annotated[schemas.User, Depends(get_current_user)],taskid:int,request:schemas.TaskBase,db:Session = Depends(get_db)):
    
    return task.update_one(taskid,request,db,current_user)


@router.delete("/delete_task/{taskid}",status_code=status.HTTP_200_OK)
def delete_task(current_user: Annotated[schemas.User, Depends(get_current_user)],taskid:int,db:Session = Depends(get_db)):

    return task.delete_one(taskid,db,current_user)

