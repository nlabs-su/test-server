# task-server

**task-server** - веб-сервер для тестового задания **TaskManager**.

### Требования

- Через терминал: python (3.10)
- В контейнере: docker

### Установка

Локально через терминал:

1. Загрузим актуальную версию, перейдем в папку проекта:

    ``git clone <ссылка на этот репозиторий>``

2. Создадим виртуальное пространство:

    ``python3 -m venv venv``
   
3. Активируем виртуальное пространство:

    ``source venv/bin/activate``

3. Установим пакеты.

    ``pip install -r requirements.txt``

Через Docker:

1. Собираем контейнер:

   `docker build --tag test-server .`


### Конфигурация сервера

Создаем файл **.env** в корне проекта

_Пример можно увидеть в .env.example_

### Запуск

#### Терминал

Запуск:

`litestar --app app.main:app run`

#### Docker

Запуск:

   `docker run --env-file .env --network=host --name test -v $(pwd)/appdata:/appdata test-server`

###  Документация

После запуска сервера доступна автособираемая документация.
* Swagger UI - **<SERVER_HOST:SERVER_PORT>/schema/swagger**
* Redoc- **<SERVER_HOST:SERVER_PORT>/schema/redoc**
* Elements - **<SERVER_HOST:SERVER_PORT>/schema/elements**