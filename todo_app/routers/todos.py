import sys
sys.path.append("..")

from typing import Optional
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from dto.todos import Todo
from .auth import get_current_user, get_user_exception
from exceptions.todo import successful_response,http_Exception


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404:{"description":"Not found"}}
)
        
@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@router.get("/user",)
async def read_by_user(user:dict = Depends(get_current_user) , db : Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

@router.get("/{todo_id}")
async def read_todo(todo_id : int , db:Session = Depends(get_db)):
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_Exception()

@router.post("/")
async def create_todo(todo:Todo,user : dict = Depends(get_current_user), db:Session = Depends(get_db)):
    todo_Model = models.Todos()
    todo_Model.title = todo.title
    todo_Model.description = todo.description
    todo_Model.priorty = todo.priorty
    todo_Model.complete = todo.complete
    todo_Model.owner_id = user.get("id")
    db.add(todo_Model)
    db.commit()
    return successful_response(201)

@router.put("/{todo_id}")
async def update_todo(todo_id : int ,  todo:Todo,user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise http_Exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priorty = todo.priorty
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()
    return successful_response(200)

@router.delete("/{todo_id}")
async def delete_todo(todo_id : int , user : dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise http_Exception()
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return successful_response(200)
    

