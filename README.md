# Дипломный проект FOODGRAM🍔 
![example workflow](https://github.com/tapp41k/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### 📖Описание
Проект Foodgram «Продуктовый помощник». Онлайн-сервис где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### 🛠️Используемые технологии
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHubActions](https://img.shields.io/badge/GitHub_Actions-black?style=for-the-badge&logo=github-actions&logoColor=white)
![YandexCloud](https://img.shields.io/badge/Yandex_Cloud-FFD43B?style=for-the-badge&logo=yandex-cloud&logoColor=white)
### 📝Инструкция по развёртыванию:
1. Загрузите проект.
```
git clone git@github.com:tapp41k/foodgram-project-react.git
```
2. Подключиться к вашему серверу.
```
ssh <server user>@<server IP>
```
3. Установите Докер на свой сервер.
```
sudo apt install docker.io
```
4. Получить разрешения для docker-compose.
```
sudo chmod +x /usr/local/bin/docker-compose
```
5. Создайте каталог проекта.
```
mkdir foodgram && cd foodgram/
```
6. Создайте env-файл.
```
touch .env
```
7. Заполните env-файл.
```

DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY='' указываем секретный ключ Django из файла settings.py
DEBUG=False
ALLOWED_HOSTS=127.0.0.1 ваш_хост ваш_домен localhost

DB_ENGINE=django.db.backends.postgresql

```
8. Скопируйте файлы из 'infra/' с ПК на ваш сервер.
```
scp infra/* <server user>@<server IP>:/home/<server user>/foodgram
```
9. Запустите docker-compose.
```
sudo docker compose -f docker-compose.yml up -d
```
10. Запустите миграции.
```
sudo docker compose -f docker-compose.yml exec backend python manage.py makemigrations
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```
11. Запустите сбор статики.
```
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic --no-input
```
12. Создайте супер пользователя.
```
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```
13. Загрузите подготовленный список ингредиентов для работы с проектом
```
sudo docker compose -f docker-compose.yml exec backend python manage.py load_json_data
```

### ✅Настроен Workflow, который состоит из четырех шагов:
- Проверка кода на соответствие PEP8
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.

### 🔓Actions secrets
- `DOCKER_PASSWORD` = пароль от DockerHub
- `DOCKER_USERNAME` = логин DockerHub
- `HOST` = адрес вашего удаленного сервера
- `SSH_KEY` = Ключ для подключения к серверу
- `TELEGRAM_TO` = ваш id в телеграме
- `TELEGRAM_TOKEN` = токен телеграм бота
- `USER` = логин на вашем удаленном сервере
- `PASSPHRASE` = пароль от сервера

<h2>🚀Проект доступен по адресу 
<a href="https://foodgramn1.sytes.net/" target="_blank">FOODGRAM</a></h2>

### 🛡️Данные для входа в админку:
```
Логин: admin@yandex.ru
Пароль: admin
```
<h2> Автор проекта </a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32" width="32"/></h2>

[Илья Осадчий](https://github.com/tapp41k)
