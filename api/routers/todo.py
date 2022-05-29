from fastapi import Response, status, HTTPException, Depends, APIRouter

from api import oauth2
from ..models import todo
from .. import schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import false, func
from typing import  List, Optional

router = APIRouter(
    prefix="/todo",
    tags=['Todo']
)

@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int=10, skip:int = 0, search:Optional[str] = ""):
    todos = db.query(todo.TodoModel).group_by(todo.TodoModel.todo_id).filter(todo.TodoModel.user_id == user.user_id).filter(todo.TodoModel.todo_text.contains(search)).filter(todo.TodoModel.is_active == True).limit(limit).offset(skip).all()
    if not todos:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"todo not Exists for the user")
    return todos

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoResponse)
def create_post(todos: schemas.TodoBase, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    new_todo = todo.TodoModel(user_id = user.user_id,**todos.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/{id}", response_model=schemas.TodoResponse)
def get_post(id : int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    todos = db.query(todo.TodoModel).filter(todo.TodoModel.todo_id == id).filter(todo.TodoModel.user_id == user.user_id).filter(todo.TodoModel.is_active == True).first()
    if not todos:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"todo with id: {id} not Exists for the user")
    return todos

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    todo_query = db.query(todo.TodoModel).filter(todo.TodoModel.todo_id == id)
    todos = todo_query.first()
    if not todos:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"todo with id: {id} not Exists")
    if todos.user_id != user.user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not Authorized")
    todo_query.update({'is_active' : False}, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TodoResponse)
def update_post(id: int, todos: schemas.CreateTodo, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    todo_query = db.query(todo.TodoModel).filter(todo.TodoModel.todo_id == id)
    todo1 = todo_query.first()
    if not todo1:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"todo with id: {id} not Exists")
    if todo1.user_id != user.user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not Authorized")
    todo_query.update(todos.dict(), synchronize_session=False)
    db.commit()
    return todo_query.first()