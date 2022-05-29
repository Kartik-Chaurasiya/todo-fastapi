from datetime import datetime, timedelta
from . import schemas, database
from jose import JWTError, jwt
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from .models import user

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#secretkey
#algo
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    users = db.query(user.UserModel).filter(user.UserModel.user_id == token.user_id).first()
    return users