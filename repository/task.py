
from loguru import logger
from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from oauth2 import get_current_user



def add_task(request: schemas.Task, db: Session,c_user):
    addTask = models.Task(title=request.title,description=request.description,due_date=request.due_date,status=request.status,user_id=c_user.id)
    db.add(addTask)
    db.commit()
    db.refresh(addTask)
    return addTask

def get_one(id:int,db: Session):
    single_task = db.query(models.Task).join(models.User).filter(models.Task.id == id , models.User.is_delete == False).first()
    if not single_task :
        logger.error(f"No task found for id at {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return single_task


def get_all(db: Session):
    all_tasks = db.query(models.Task).join(models.User).filter(models.User.is_delete == False).all()
    print("alltasks --------------> ",all_tasks)
    if not all_tasks :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_tasks


def update_one(task_id, request, db, current_user):

    if current_user.role == "regular":
        update_task = db.query(models.Task).join(models.User).filter(models.Task.id == task_id,models.User.is_delete == False).first()
    elif current_user.role == "admin":
        update_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if not update_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task with ID {task_id} found")

    update_task.title = request.title
    update_task.description = request.description
    update_task.due_date = request.due_date
    update_task.status = request.status
    db.commit()
    db.refresh(update_task)
    return update_task


def delete_one(task_id, db, current_user):

    if current_user.role == "regular":
        todelete_task = db.query(models.Task).join(models.User).filter(models.Task.id == task_id,models.User.is_delete == False, models.Task.user_id == current_user.id).first()
    elif current_user.role == "admin":
        todelete_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    if not todelete_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task with ID {task_id} found or you are not authorize to make changes to id {task_id}")
    db.delete(todelete_task)
    db.commit()

    return {'msg': f"Task was Deleted at {task_id}"}

