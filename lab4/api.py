import asyncio
import os
import httpx
from dotenv import load_dotenv
import time

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API-ключей из переменных окружения
API_KEY_ruGPT: str = os.getenv("ruGPT_TRANSLATE_API_KEY", "")
API_KEY_LLAMA: str = os.getenv("LLaM_TRANSLATE_API_KEY", "")


# Асинхронная функция для получения рекомендации с использованием RuGPT-3
async def get_recomendation_from_rugpt(
    genre: str, author: str, wish: str, retries: int = 6, init_delay: float = 0.5
) -> str:
    """
    Асинхронная функция для получения рекомендации с использованием RuGPT-3.

    Аргументы:
    - genre (str): жарн книги.
    - author (str): автор книги.
    - wish (str): язык перевода (по умолчанию "en").
    - retries (int): количество повторных попыток при ошибке.
    - init_delay (float): начальная задержка между повторными попытками (в секундах).

    Возвращает:
    - str: рекомендация книги.
    """

    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {API_KEY_ruGPT}"}

    # Подготовка данных для отправки на API
    prompt = f"Порекомендуй на русском языке книгу за авторством {author} в жанре {genre} с учётом пожелания '{wish}'"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 80,  # Увеличим длину ответа для перевода
            "temperature": 0.8,  # "Творчество" генерации
        },
    }

    for attempt in range(retries):
        success = False
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Проверяем на ошибки HTTP
                result = response.json()

                # Проверяем структуру ответа
                if isinstance(result, list) and len(result) > 0:
                    print(result)
                    if "generated_text" in result[0]:
                        success = True
                        return result[0]["generated_text"]
                    else:
                        raise ValueError(f"Неизвестный формат ответа API: {result}")
                else:
                    raise ValueError(f"Некорректный ответ от API: {result}")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 503:
                    internal_error = f"HTTP ошибка 503: Сервис временно недоступен. Попытка {attempt + 1} из {retries}."
                    response = "Ошибка 503: Сервис временно недоступен."
                else:
                    internal_error = f"HTTP ошибка: {e.response.status_code}\nТекст ошибки: {e.response.text}"
                    response = (
                        f"Ошибка HTTP {e.response.status_code}: {e.response.text}"
                    )
            except httpx.RequestError as e:
                internal_error = f"Ошибка запроса: {e}"
                if e.request:
                    internal_error += f"\nURL запроса: {e.request.url}\nТело запроса: {e.request.content.decode('utf-8')}"
                response = "Ошибка: проблема с запросом к API."
            except ValueError as e:
                response = internal_error = f"Ошибка обработки ответа API: {e}"
            finally:
                if not success:
                    if attempt < retries:
                        print(internal_error)
                        await asyncio.sleep(
                            init_delay * 2**attempt
                        )  # Задержка перед повторной попыткой
                    else:
                        return response


# Асинхронная функция для получения рекомендации с использованием LLaMA API
async def get_recomendation_from_llama(
    genre: str, author: str, wish: str, retries: int = 6, init_delay: float = 0.5
) -> str:
    """
    Аргументы:
    - genre (str): жарн книги.
    - author (str): автор книги.
    - wish (str): язык перевода (по умолчанию "en").
    - retries (int): количество повторных попыток при ошибке.
    - init_delay (float): начальная задержка между повторными попытками (в секундах).

    Возвращает:
    - str: рекомендация книги.
    """
    url = "https://llama-3.p.rapidapi.com/llama3"
    headers = {
        "x-rapidapi-key": API_KEY_LLAMA,
        "x-rapidapi-host": "llama-3.p.rapidapi.com",
        "Content-Type": "application/json",
    }

    # Формируем prompt
    prompt = f"Порекомендуй на русском языке книгу за авторством {author} в жанре {genre} с учётом пожелания '{wish}'"

    payload = {
        "prompt": wish,
        "system_prompt": prompt,
    }
    for attempt in range(retries):
        success = False
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Проверка на ошибки
                result = response.json()

                # Извлекаем текст из ответа
                if "msg" in result:
                    success = True
                    return result["msg"]
                else:
                    response = internal_error = "Ошибка: не удалось получить перевод."
            except httpx.HTTPStatusError as e:
                # Обработка ошибок HTTP
                internal_error = f"HTTP ошибка: {e.response.status_code}\nТекст ошибки: {e.response.text}"
                response = f"Ошибка HTTP {e.response.status_code}: {e.response.text}"
            except httpx.RequestError as e:
                # Обработка ошибок запроса
                internal_error = f"Ошибка запроса: {e}"
                if e.request:
                    internal_error += f"\nURL запроса: {e.request.url}\nТело запроса: {e.request.content.decode('utf-8')}"
                response = "Ошибка: проблема с запросом к API."
            except Exception as e:
                # Обработка неизвестных ошибок
                internal_error = f"Неизвестная ошибка: {e}"
                response = f"Ошибка: {e}"
            finally:
                if not success:
                    if attempt < retries:
                        print(internal_error)
                        await asyncio.sleep(
                            init_delay * 2**attempt
                        )  # Задержка перед повторной попыткой
                    else:
                        return response
