@echo off
REM Activate the virtual environment and run uvicorn with FastAPI app
call "D:\Learn at DPA\ToDoList\todo_API\todoenv\Scripts\activate.bat" &&  python -m uvicorn main:app --reload
 