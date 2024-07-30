import sys
sys.path.append("..")

import os
from dotenv import load_dotenv
from fastapi import Depends, APIRouter
from typing import Optional
import models
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
from helpers.auth import get_password_hashed,verify_password,authenticate_user,create_access_token 
from exceptions.auth import get_user_exception,token_exception
from dto.user import User

oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user":"Not authorized"}}
)



@router.post("/create/user")
async def create_new_user(create_user : User, db : Session = Depends(get_db)):
    create_user_model =models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_password = get_password_hashed(create_user.password)
    create_user_model.is_active = True
    
    db.add(create_user_model)
    db.commit()
    
    return create_user_model

@router.post("/token")
async def login_for_access_token(form_data :OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user  = authenticate_user(form_data.username , form_data.password,db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username , user.id , token_expires)
    return {"token":token}

async def get_current_user(token : str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token,os.getenv('SECRET_KEY'),os.getenv('ALGORITHM'))
        username : str = payload.get("username")
        user_id :int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username":username, "id":user_id}
    except JWTError:
        raise get_user_exception()