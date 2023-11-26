Для запуска проекта необходимо:
- Настроить виртуальное окружение
  ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Установить зависимости проекта
    ```bash
    pip install -r requirements.txt
    ```
- Запустить контейнер с базой данных
    ```bash
  docker compose up --build -d
    ```
- Запустить сервис базы данных
    ```bash
  python3 db_service.py
    ```
- Запустить сервис парсинга
    ```bash
  python3 parser_service.py
    ```

Данные для входа в базу данных:
```
db: Apache Cassandra
host: localhost
port: 9042
```