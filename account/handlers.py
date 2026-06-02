from fastapi import  APIRouter, HTTPException, Depends
from core.chemas import UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,exists
from jose import jwt

from db import LocalSession
from models import User

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta,timezone

load_dotenv()
secret_key = os.getenv('SECRET_KEY')

account_router = APIRouter(prefix= '/users' , tags=['логин и регистрация'])

async def get_db():
    async with LocalSession() as session:
        yield session

@account_router.post('/register')
async def register(data : UserCreate, db: AsyncSession = Depends(get_db)):  #передаем схему для валидации + сессию бд
    result = await db.execute(select(exists().where(User.email == data.email)))
    existing = result.scalar()
    if existing:
        raise HTTPException(status_code=400, detail= 'Пользователь с таким email уже существует')

    new_user = User(**data.model_dump())
    db.add(new_user)
    await db.commit()

    return {'message':'Пользователь создан','email':new_user.email}

@account_router.post('/login')
async def login(data : UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code= 401, detail= 'Неверный Email или пароль')
    if existing.password != data.password:
        raise HTTPException(status_code=401, detail='Неверный Email или пароль')

    payload = {
        'sub': existing.email,
        'exp': datetime.now(timezone.utc)+timedelta(hours= 24)
    }

    token = jwt.encode(payload, secret_key, algorithm= 'HS256')

    return {'access_token': token, 'token_type': 'bearer'}