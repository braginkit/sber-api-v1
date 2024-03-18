### Запуск в докере
> make run

### Примеры запросов
Получение данных
>curl --location 'http://0.0.0.0:8080/visited_domains/?from=0&to=9876543210'

Вставка данных
> curl --location 'http://0.0.0.0:8080/visited_links/' --header 'Content-Type: application/json' --data '{
    "links": [
        "https://ya.ru/",
        "https://ya.com/",
        "https://ya.dw/"
    ]
}'

### Разработка
Зависимости
> python3.9 -m pip install -r requirements/requirements.txt

Запуск
> cd api \
> python3.9 main.py

### Запуск тестов
> python3.9 -m pip install -r requirements/requirements.txt \
> python3.9 -m pip install -r requirements/requirements_test.txt \
> cd api \
> python3.9 -m pytest test.py --disable-pytest-warnings -vv --durations=0