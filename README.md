# Решение тестового задания для Компании EM

## Описание

Проект **TestEM** демонстрирует навыки работы с  `FastAPI`  с подключением БД `PostgreSQL` и инструментами тестирования, такими как `pytest`. Проект включает Docker Compose для развертывания приложения и базы данных в контейнерах.

## Запуск проекта

### Требования
- Docker и Docker Compose
- Python 3.11+

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/curabby/TestEM.git
cd TestEM
```
2. Запустите контейнеры
Используйте Docker Compose для запуска проекта:
```bash
docker-compose up --build -d
```
## Доступ к документации Swagger
```
http://localhost:8000/docs
```

3. Автотесты
Уточните ID контейнера приложения
```bash
docker-compose ps
```
Выполните команду 
```bash
docker exec -it <ID контейнера приложения> pytest tests/
```
4. Завершение работы Docker
```bash
docker-compose down
```
