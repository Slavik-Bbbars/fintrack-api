
from fastapi import  APIRouter, HTTPException, Depends
from core.chemas import FinanceCreate, FinanceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import TransactionType
from db import LocalSession

from models import Finances,User

import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
secret_key = os.getenv('SECRET_KEY')

finance_router = APIRouter(prefix= '/finance' , tags = ['Доходы'])

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



@finance_router.post('/add', description= 'Добавляет доход')
async def add_finance( data: FinanceCreate, db: AsyncSession = Depends(get_db),
                     user: User = Depends(get_user)):
    finance = Finances(
        user_email = user.email,
        amount = data.amount,
        type = data.type,
        category = data.category,
    )
    db.add(finance)
    await db.commit()
    return {'status':'ok', 'message' : 'Доход успешно добавлен'}



@finance_router.get('/all', response_model=list[FinanceResponse], description= 'Возвращает все расходы/доходы')
async def get_all_finance(db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_user),type: TransactionType = TransactionType.INCOME):

    finances = await db.execute(select(Finances).where(Finances.user_email == user.email,
                                                       Finances.type == type))

    result = finances.scalars().all()
    return result


@finance_router.get('/month-category',response_model= list[FinanceResponse], description= 'возвращает финансы по месяцу/категории ')
async def get_finance_category_month(db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_user), category: str = '', month_bool : bool = False,
                                     type: TransactionType = TransactionType.INCOME):

    if not category and not month_bool:
        raise HTTPException(status_code= 400, detail= 'Не указан параметр выборки: месяц или категория')

    query = select(Finances).where(Finances.user_email == user.email, Finances.type == type)

    if category:
        query = query.where(Finances.category == category)
    if month_bool:
        now = datetime.now()
        month = now.month
        year = now.year
        query = query.where(
            extract('year',Finances.created_at) == year,
            extract('month', Finances.created_at) == month
        )
    result = await db.execute(query)
    return result.scalars().all()

@finance_router.delete('/{id_f}')
async def delete_finance(id_f: int, user: User = Depends(get_user), db: AsyncSession = Depends(get_db),
                         type: TransactionType = TransactionType.INCOME):
    finance = await db.execute(select(Finances).where(Finances.id_f == id_f, Finances.type == type))
    owned_finance = finance.scalar_one_or_none()
    if owned_finance is None:
        raise HTTPException(status_code=404, detail='Запись не найдена')
    if owned_finance.user_email != user.email:
        raise HTTPException(status_code= 403, detail= 'Нет доступа')
    await db.delete(owned_finance)
    await db.commit()
    return {'status': 'ok', 'message': 'запись удалена'}

