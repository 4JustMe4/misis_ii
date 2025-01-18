import asyncio
import os
import httpx
from dotenv import load_dotenv
import time
from bookdb import Database

# Загрузка переменных окружения из .env файла
load_dotenv()

db = Database('var/db.sqlite3')

def add_record(uid, book_uid, grade) -> None:
    put_grade(uid, book_uid, grade)

def get_recomendation(uid) -> str:
    return "456"

def get_book_name(book_uid) -> str:
    rs = db.get_book(book_uid)
    if type(None) == type(rs):
      return None
    book_name = rs[1]
    return book_name

def restart_user(uid) -> None:
    db.del_grades(uid)
    db.del_last(uid)
