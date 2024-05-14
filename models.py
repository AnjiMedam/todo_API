from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from sqlalchemy.orm import relationship
import models,database
from database import Base

# User model: id, username, email, password, role
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(100),unique=True)
    email = Column(String(100))
    password = Column(String(100))
    role=Column(String(100),default="regular")
    is_delete= Column(Boolean,default=False)

    tasks = relationship('Task', back_populates="creator",cascade="all, delete")

#  Task model: id, title, description, due_date, status, user_id (foreign key)
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(100))
    due_date = Column(Date)
    status=Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    creator = relationship("User", back_populates="tasks")



    

    




