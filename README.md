# Welbex - Тестовое задание web-программист Python (Middle)

[Текст задания](https://faint-adasaurus-4bc.notion.site/web-Python-Middle-c1467cf373c24f0cafb8bfe0fe77cc79).
Реализованы оба уровня.

## Установка и запуск

Запустите базу данных и сайт:

```shell-session
$ docker-compose up
```

В новом терминале не выключая сайт запустите команды для настройки базы данных:

```shell-session
$ docker-compose run web ./manage.py migrate
$ docker-compose run web ./manage.py createsuperuser
```

Для тонкой настройки используйте переменные окружения.
## Переменные окружения

Образ с Django считывает настройки из переменных окружения:

`SECRET_KEY` -- Секретный ключ Django, см. документацию.  
`DJANGO_DEBUG` -- настройка Django для включения отладочного режима. Принимает значения `TRUE` или `FALSE`.  
`DJANGO_ALLOWED_HOSTS` -- настройка Django со списком разрешённых адресов. Если запрос прилетит на другой адрес, то сайт ответит ошибкой 400. Можно перечислить несколько адресов через запятую, например `127.0.0.1,192.168.0.1,site.test`.   
`POSTGRES_DB` -- имя базы данных PostgreSQL. Другие СУБД сайт не поддерживает.  
`POSTGRES_USER` -- имя пользователя базы данных PostgreSQL.  
`POSTGRES_PASSWORD` -- пароль пользователя базы данных PostgreSQL.  
`POSTGRES_URL` -- адрес для подключения к базе данных PostgreSQL. Другие СУБД сайт не поддерживает. [Формат записи](https://github.com/jacobian/dj-database-url#url-schema).  

## Использование

Схема API доступна по адресу [127.0.0.1:8000/swagger-ui](http://127.0.0.1:8000/swagger-ui)