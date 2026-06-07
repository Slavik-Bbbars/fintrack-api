
from fastapi import  APIRouter, HTTPException, Depends
from core.chemas import FinanceCreate, FinanceResponse, FinancePaginated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


from models import TransactionType
from models import Finances,User
from core.dependencies import get_db, get_user

from datetime import datetime


finance_router = APIRouter(prefix= '/finance' , tags = ['Доходы'])





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



@finance_router.get('/all', description= 'Возвращает все расходы/доходы за текущий год или пагинированные')
async def get_all_finance(db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_user),type: TransactionType = TransactionType.INCOME,
                          limit : int | None= None, offset : int = 0):

    query = select(Finances).where(Finances.user_email == user.email,
                                                       Finances.type == type)
    if limit is None:
        year = datetime.now().year
        query = query.where( Finances.created_at >= datetime(year, 1, 1),
                             Finances.created_at < datetime(year+1, 1, 1))
        finances = await db.execute(query)
        return finances.scalars().all()
    else:
        count = await db.execute(select(func.count()).where(Finances.user_email == user.email,
                                                       Finances.type == type))
        total = count.scalar()
        query = query.limit(limit).offset(offset)
        finances = await db.execute(query)
        return {
            'items': finances.scalars().all(),
            'total' : total,
            'limit' : limit,
            'offset' : offset
        }


@finance_router.get('/month-category',response_model= list[FinanceResponse], description= 'возвращает финансы по месяцу/категории ')
async def get_finance_category_month(db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_user), category: str = '', month_bool : bool = False,
                                     type: TransactionType = TransactionType.INCOME):

    if not category and not month_bool:
        raise HTTPException(status_code= 400, detail= 'Не указан параметр выборки: месяц или категория')

    query = select(Finances).where(Finances.user_email == user.email, Finances.type == type)

    if category:
        year = datetime.now().year
        query = query.where(Finances.category == category,
                            Finances.created_at >= datetime(year, 1, 1),
                            Finances.created_at < datetime(year+1, 1, 1))
    if month_bool:
        now = datetime.now()
        first_day = datetime(now.year, now.month, 1)
        if now.month == 12:
            next_month = datetime(now.year + 1, 1, 1)
        else:
            next_month = datetime(now.year, now.month + 1, 1)
        query = query.where(
            Finances.created_at >= first_day,
                        Finances.created_at < next_month
        )
    result = await db.execute(query)
    return result.scalars().all()


@finance_router.delete('/{id_f}')
async def delete_finance(id_f: int, user: User = Depends(get_user), db: AsyncSession = Depends(get_db),
                         ):
    finance = await db.execute(select(Finances).where(Finances.id_f == id_f))
    owned_finance = finance.scalar_one_or_none()
    if owned_finance is None:
        raise HTTPException(status_code=404, detail='Запись не найдена')
    if owned_finance.user_email != user.email:
        raise HTTPException(status_code= 403, detail= 'Нет доступа')
    await db.delete(owned_finance)
    await db.commit()
    return {'status': 'ok', 'message': 'запись удалена'}

