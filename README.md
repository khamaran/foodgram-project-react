# Проект Foodgram

## Адрес
http://khamafoodgram.didns.ru

- Логин администратора: khamaran@yahoo.com
- Пароль администратора: Tomnam1997!

## Описание

Foodgram - приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.  Проект использует базу данных PostgreSQL. Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на сервере. Образ с проектом загружается на Docker Hub.

## Пользовательские роли

### Гость (неавторизованный пользователь)

Что могут делать неавторизованные пользователи:

- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

### Уровни доступа пользователей:
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор 

### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

### Что может делать администратор
- Администратор обладает всеми правами авторизованного пользователя. 
- Плюс к этому он может:
  - изменять пароль любого пользователя,
  - создавать/блокировать/удалять аккаунты пользователей,
  - редактировать/удалять любые рецепты,
  - добавлять/удалять/редактировать ингредиенты.
  - добавлять/удалять/редактировать теги.


## Ресурсы API Foodgram

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс tags: получение данных тега или списка тегов рецепта.
- Ресурс recipes: создание/редактирование/удаление рецептов, а также получение списка рецептов или данных о рецепте.
- Ресурс shopping_cart: добавление/удаление рецептов в список покупок.
- Ресурс download_shopping_cart: cкачать файл со списком покупок.
- Ресурс favorite: добавление/удаление рецептов в избранное пользователя.
- Ресурс subscribe: добавление/удаление пользователя в подписки.
- Ресурс subscriptions: возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
- Ресурс ingredients: получение данных ингредиента или списка ингредиентов.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/khamaran/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейдите в папку backend/:
```
cd backend/
```

Выполнить миграции:

```
python3 manage.py migrate
```

Установить переменную окружения:

В директории проекта foodgram-project-react/backend создайте файл .env и запишите в него
полученную переменную в формате ключ=значение:

  ```python
  SECRET_KEY=abcnfhgijfkg
  DB_PORT=5432
  POSTGRES_DB=kittygram
  POSTGRES_USER=kittygram_user
  POSTGRES_PASSWORD=kittygram_password
  DB_HOST=db_kittygram
  ```

Файл .env должен лежать в той же директории, что и settings.py!

Запустить проект:

```
python3 manage.py runserver
```
## Документация

В папке infra выполните команду:

```
docker-compose up
```

При выполнении этой команде сервис frontend, описанный в docker-compose.yml подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу. 
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/


## Создание образа

Запустите терминал. Убедитесь, что вы находитесь в той же директории, где сохранён Dockerfile, и запустите сборку образа:
docker build -t foodgram .  
build — команда сборки образа по инструкциям из Dockerfile.
-t foodgram — ключ, который позволяет задать имя образу, а потом и само имя.
. — точка в конце команды — путь до Dockerfile, на основе которого производится сборка..


## Развёртывание проекта в нескольких контейнерах

Инструкции по развёртыванию проекта в нескольких контейнерах пишут в файле docker-compose.yaml. 
Убедитесь, что вы находитесь в той же директории, где сохранён docker-compose.yaml и запустите docker-compose командой docker-compose up. У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres.


## Стек технологий

- asgiref==3.7.2
- atomicwrites==1.4.1
- attrs==23.1.0
- certifi==2023.5.7
- cffi==1.15.1
- charset-normalizer==3.2.0
- colorama==0.4.6
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==41.0.1
- defusedxml==0.7.1
- Django==3.2.3
- django-templated-mail==1.1.1
- djangorestframework==3.12.4
- django-filter~=23.1
- djoser==2.1.0
- idna==3.4
- iniconfig==2.0.0
- itypes==1.2.0
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- oauthlib==3.2.2
- packaging==23.1
- Pillow==9.0.0
- pluggy==0.13.1
- psycopg2-binary==2.9.3
- py==1.11.0
- pycparser==2.21
- PyJWT==2.7.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- python-dotenv==1.0.0
- python3-openid==3.2.0
- pytz==2023.3
- PyYAML==6.0
- requests==2.31.0
- requests-oauthlib==1.3.1
- six==1.16.0
- social-auth-app-django==4.0.0
- social-auth-core==4.4.2
- sqlparse==0.4.4
- toml==0.10.2
- typing_extensions==4.7.1
- uritemplate==4.1.1
- urllib3==2.0.3
- webcolors==1.11.1


# Примеры запросов

### Профиль пользователя

**Авторизация по токену. Все запросы от имени пользователя должны выполняться с заголовком "Authorization: Token TOKENVALUE".**

*[GET] /api/users/{id}/*

*Пример ответа:*
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```

### Список ингредиентов

**Список ингредиентов с возможностью поиска по имени.**

*[GET] /api/ingredients/*

*Пример ответа:*
```
{
  "id": 0,
  "name": "Капуста",
  "measurement_unit": "кг"
}
```

## Автор

Мария Тумилович
