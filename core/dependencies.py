from jose import jwt, JWTError
from db import LocalSession
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from fastapi import  HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import os
from dotenv import load_dotenv

from models import User


load_dotenv()
secret_key = os.getenv('SECRET_KEY')

security = HTTPBearer()

async def get_db():
    async with LocalSession() as session:
        yield session

async def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)): #достаем юзера из токена
    token = credentials.credentials
    try:
        payload = jwt.decode(token,secret_key, algorithms= ['HS256'])
        email : str = payload.get('sub')
        if (not email):
            raise HTTPException(status_code= 401, detail= 'Невалидный токен!')
    except JWTError:
        raise HTTPException(status_code=401, detail='Невалидный токен!')

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code= 401, detail= 'Пользователь не найден')
    return user
