from pydantic import BaseModel, field_validator, EmailStr,Field
from pydantic.v1 import ConfigDict

from .categories import ExpenseCategory, IncomeCategory
from datetime import datetime
from models import TransactionType



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name : str
    surname : str
    email : EmailStr
    password : str

    model_config = ConfigDict(extra= 'forbid')

class FinanceCreate(BaseModel):
    amount : float = Field(gt=0)
    type : TransactionType
    category : str

    @field_validator('category')
    @classmethod
    def validate_category(cls, v,values):
        transaction_type = values.data.get('type')
        if transaction_type == 'income':
            valid = [c.value for c in IncomeCategory]
        else:
            valid = [c.value for c in ExpenseCategory]
        if v not in valid:
            raise ValueError(f'Категория должна быть в одной из: {valid}')
        else:
            return v

    model_config = ConfigDict(extra='forbid')

class FinanceResponse(BaseModel):
    id_f : int
    user_email: str
    amount: float
    type: str
    category : str
    created_at: datetime

    model_config = {'from_attributes': True}  #возможность читать поля как атрибуты