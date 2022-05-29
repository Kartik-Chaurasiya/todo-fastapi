from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, utils
from ..models import user
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import  List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(users: schemas.CreateUser, db: Session = Depends(get_db)):

    # hash password
    users.password = utils.hash(users.password)
    
    new_user = user.UserModel(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_post(id : int, db: Session = Depends(get_db)):
    post = db.query(user.UserModel).filter(user.UserModel.user_id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} not Exists")
    return post