## Установитие переменные окружения
### Переменные Django
`DJANGO_DEBUG`

`DJANGO_SECRET_KEY` 

`DJANGO_ALLOWED_HOSTS`
### Переменные базы данных
`SQL_ENGINE`

`SQL_DATABASE` - имя базы данных

`SQL_USER` - имя пользователя

`SQL_PASSWORD` - пароль

`SQL_HOST` - хост

`SQL_PORT` - порт
## Запуск приложения
### Для запуска локально
```
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
```
Создаем админа
```
python manage.py createsuperuser
```
Запускаем сервер
```
python manage.py runserver
```
### Для звпуска в Docker
```
docker-compose up --build
```
Создаем админа
```
docker-compose run web python manage.py createsuperuser
```
## Документация
host:port/api/v1/doc/