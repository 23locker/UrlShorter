# UrlShorter 🔗

Сервис для сокращения длинных URL в короткие ссылки.

## Стек

- **Backend**: FastAPI
- **БД**: PostgreSQL + SQLAlchemy
- **Драйвер**: asyncpg
- **Сервер**: Uvicorn
- **Тесты**: pytest

## Запуск

### Вариант 1: Docker Compose + Локальный сервер

1. Запустить PostgreSQL в Docker:

```bash
git clone https://github.com/23locker/UrlShorter.git
cd UrlShorter
docker-compose up -d
```

2. Установить зависимости:

```bash
pip install -e .
```

или с uv:

```bash
uv sync
```

3. Запустить приложение:

```bash
# С pip
uvicorn src.main:app --reload

# С uv
uv run uvicorn src.main:app --reload
```

Приложение будет доступно на `http://localhost:8000`

## Использование

Откройте `http://localhost:8000` в браузере и используйте веб-интерфейс.

**Или через API:**

```bash
curl -X POST http://localhost:8000/short_url \
  -H "Content-Type: application/json" \
  -d '{"user_url": "https://example.com/path"}'
```

Ответ:

```json
{
  "data": "aBcDeF"
}
```

Откройте `http://localhost:8000/aBcDeF` для редиректа.

## Тестирование

```bash
pytest
```

## Структура

```
src/
├── main.py           # FastAPI приложение
├── service.py        # Основная логика
├── shortener.py      # Генерация слагов
├── exceptions.py     # Ошибки
└── database/
    ├── models.py     # ORM модели
    ├── crud.py       # Операции с БД
    └── db.py         # Конфиг БД
```
