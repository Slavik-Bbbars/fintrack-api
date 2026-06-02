import enum

class ExpenseCategory(str, enum.Enum):
    # Расходы
    FOOD = "Продукты"
    TRANSPORT = "Транспорт"
    HOUSING = "Жильё и ЖКХ"
    HEALTH = "Здоровье"
    ENTERTAINMENT = "Развлечения"
    CLOTHING = "Одежда"
    EDUCATION = "Образование"
    SPORT = "Спорт"
    CAFE = "Кафе и рестораны"
    TRAVEL = "Путешествия"
    TECH = "Техника"
    OTHER = "Другое"

class IncomeCategory(str, enum.Enum):
    # Доходы
    SALARY = "Зарплата"
    FREELANCE = "Фриланс"
    GIFT = "Подарок"
    INVESTMENT = "Инвестиции"
    OTHER = "Другое"