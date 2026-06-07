from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

'''Настройка сессионного подключения к бд'''

load_dotenv()

DB_url = os.getenv('DATABASE_URL')
engine = create_async_engine(DB_url, echo = False)

LocalSession = async_sessionmaker(engine, expire_on_commit= False) #ласт параметр для того чтобы сохранять модель в памяти

class Base(DeclarativeBase):
    pass

