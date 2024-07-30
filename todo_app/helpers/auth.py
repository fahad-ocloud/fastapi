from fastapi import Depends
from datetime import datetime,timedelta
from typing import Optional
from passlib.context import CryptContext
import models
import os
from jose import jwt

bcrypt_context= CryptContext(schemes=["bcrypt"])

def get_password_hashed(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password , hashed_password):
    return bcrypt_context.verify(plain_password , hashed_password)

def authenticate_user(username:str , password:str ,db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not  verify_password(password , user.hashed_password):
        return False
    return user

def create_access_token(username:str , user_id:int , expires_delta : Optional[timedelta] = None):
    encode = {"username" : username , "id":user_id}
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,key= os.getenv('SECRET_KEY'),algorithm=os.getenv('ALGORITHM'))

