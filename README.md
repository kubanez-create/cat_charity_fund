# Cat Charity Fund

Backend приложение для благотворительного фонда, на текущий момент позволяет зарегистрированным пользователям:

- Просматривать список активных благотворительных проектов.
- Создавать пожертвования.
- Просматривать список своих пожертвований.

Пользователи с правами администратора также могут:
- Создавать новые благотворительные проекты.
- Изменять существующие благотворительные проекты.
- Закрывать благотворительные проекты, в которые еще никто не инвестировал.
- Просматривать список всех пожертвований.


## Стек технологий
- Python
- FastAPI
- FastAPI Users
- Pydantic
- SQLAlchemy
- Alembic

## Зависимости
- Перечислены в файле backend/requirements.txt

## Для запуска на собственном сервере последовательно выполните команды

1. Клонируйте данный репозиторий `git clone git@github.com:kubanez-create/cat_charity_fund.git`
2. Перейдите в созданную папку `cd cat_charity_fund`
3. Создайте и активируйте виртуальное окружение
```bash
python3 -m venv env
source env/bin/activate
```
4. Устаноте зависимости `pip install -r requirements.txt`;
5. Запустите приложение `uvicorn app.main:app`.

## Автор

- [Костенко Станислав](https://github.com/kubanez-create) 
