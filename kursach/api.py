import asyncio
import os
import httpx
from dotenv import load_dotenv
import time

# Загрузка переменных окружения из .env файла
load_dotenv()

def add_record(uid, book_uid, grade) -> None:
    pass

def get_recomendation(uid) -> str:
    return "456"

def get_book_name(book_uid) -> str:
    return "New book"

def restart_user(uid) -> None:
    pass