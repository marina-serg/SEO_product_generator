# SEO Product Generator

Сервис для генерации SEO-карточек технических товаров с помощью Gemini API.

## Запуск

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Создать файл `.env`:
   ```bash
   cp .env.example .env
   ```

3. Указать API-ключ Gemini в `.env`.

4. Запустить сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Открыть документацию API: http://127.0.0.1:8000/docs

## API

### Генерация SEO-карточки

`POST /api/products/generate`

Принимает JSON с исходными данными товара и возвращает SEO-карточку.
