# fintrack-api

Минималистичный REST API для учёта личных финансов — доходов и расходов по категориям.

---

## Стек

- **FastAPI** — основной фреймворк
- **SQLAlchemy** (async) — ORM для работы с БД
- **PostgreSQL** — база данных
- **JWT** — авторизация
- **Docker** — запуск базы данных

---

## Запуск

1. Клонировать репозиторий
```bash
git clone https://github.com/Slavik-Bbbars/fintrack-api.git
cd fintrack-api
```

2. Создать `.env` файл в корне проекта:
```env
POSTGRES_DB= finance
POSTGRES_USER= postgres
POSTGRES_PASSWORD= your_password
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/finance
SECRET_KEY=your_secret_key
```
> При запуске нелокально внутри Docker нужно заменить `localhost` на `db` в `DATABASE_URL`

3. Поднять базу данных:
```bash
docker-compose up -d
```

4. Применить миграции:
```bash
alembic upgrade head
```

5. Запустить сервер:
```bash
python main.py
```

Документация доступна по адресу: `http://localhost:8000/docs`

---

## Эндпоинты

### Пользователи
| Метод | Путь | Описание |
|---|---|---|
| POST | `/users/register` | Регистрация |
| POST | `/users/login` | Вход, возвращает JWT токен |

### Финансы
Все эндпоинты защищены JWT токеном. Тип записи передаётся параметром `type=income` или `type=expense` — отдельных ручек для доходов и расходов нет.

| Метод | Путь | Описание |
|---|---|---|
| POST | `/finances/add` | Добавить запись |
| GET | `/finances/all?type=` | Все записи по типу |
| GET | `/finances/month-category?type=&category=&month_bool=` | Фильтрация по категории и/или текущему месяцу |
| DELETE | `/finances/{id}` | Удалить запись |

