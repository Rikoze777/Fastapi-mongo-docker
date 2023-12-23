# Fastapi-mongo-docker

Тестовое задание по практике использования `fastapi`, `docker`, `mongoDB`, `poetry`

## Установка
1. Создайте файл `.env` с переменными:
    - MONGO_USERNAME='Example' `MongoDB db username`
    - MONGO_PASSWORD='12345' `MongoDB db password`
    - MONGO_DB='mailer' `MongoDB db name`
    - MAIL_FROM='example@yandex.ru' `email`
    - MAIL_USERNAME='example@yandex.ru' `email name`
    - MAIL_PASSWORD='password' `email password`

2. Введите команду:
```
docker compose up
```