from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, utils, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from ..models import user

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_data : OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    users = db.query(user.UserModel).filter(user.UserModel.user_name == user_data.username).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_data.password, users.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create token
    access_token = oauth2.create_access_token(data = {"user_id" : users.user_id})

    return {"access_token" : access_token, "token_type" : "bearer"}