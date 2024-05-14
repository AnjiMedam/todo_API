from fastapi import FastAPI
from typing import List
import models
import database
import uvicorn 
from routers import user,authentication,task
from loguru import logger
import sys
models.Base.metadata.create_all(bind=database.engine) 

app = FastAPI()


app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(user.router)


logger.remove()
logger.add('loguru/mylog.log', format="{time:MMMM D, YYYY > HH:mm:ss} |  {level} <level> {message}</level>")


if __name__=='__main__':

    uvicorn.run(app,host="localhost",port=8000)





