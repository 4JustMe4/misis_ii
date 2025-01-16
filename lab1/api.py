import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение API ключей из переменных окружения
RAPID_TRANSLATE_API_KEY = os.getenv("RAPID_TRANSLATE_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")

print("Rapid Translate API Key:", RAPID_TRANSLATE_API_KEY)
print("Google Translate API Key:", GOOGLE_TRANSLATE_API_KEY)


def rapid_translation(word, source_lang, target_lang):
    try:
        url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
        payload = {
            "q": word,
            "from": source_lang,
            "to": target_lang,
        }
        headers = {
            "x-rapidapi-key": RAPID_TRANSLATE_API_KEY,
            "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            translation = result[0]  # Достаем перевод из JSON ответа
            return translation
        else:
            return f"Ошибка: API ответил с кодом {response.status_code}"
    except Exception as e:
        return f"Ошибка: {str(e)}"


def google_translation(word, source_lang, target_lang):
    try:
        url = "https://google-translator9.p.rapidapi.com/v2"
        payload = {
            "q": word,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
        }
        headers = {
            "x-rapidapi-key": GOOGLE_TRANSLATE_API_KEY,
            "x-rapidapi-host": "google-translator9.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            translation = result["data"]["translations"][0]["translatedText"]
            return translation
        else:
            return f"Ошибка: API ответил с кодом {response.status_code}"
    except Exception as e:
        return f"Ошибка: {str(e)}"
