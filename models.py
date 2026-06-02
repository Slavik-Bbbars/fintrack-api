from sqlalchemy import Integer, String,ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import mapped_column,Mapped,relationship
from db import Base
import enum
from datetime import datetime, timezone

class TransactionType(str, enum.Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(Integer, primary_key= True)
    name : Mapped[str] = mapped_column(String(50), nullable= False)
    surname : Mapped[str] = mapped_column(String(50),nullable= False)
    email : Mapped[str] = mapped_column(String(100), unique= True,nullable= False)
    password : Mapped[str] = mapped_column(String, nullable= False)

    finances: Mapped[list['Finances']] = relationship('Finances', back_populates= 'user', cascade= 'all,delete-orphan')


class Finances(Base):
    __tablename__ = 'finances'

    id_f : Mapped[int] = mapped_column(Integer, primary_key= True)

    user_email : Mapped[str] = mapped_column(String(100), ForeignKey('users.email'),nullable= False )

    amount : Mapped[float] = mapped_column(Float, nullable= False)
    type : Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable= False) #расходы или доходы
    category : Mapped[str] = mapped_column(String(50), nullable= False) #конкретная категория
    created_at : Mapped[datetime] = mapped_column(DateTime, default= datetime.now())

    user : Mapped['User'] = relationship('User',back_populates= 'finances')
