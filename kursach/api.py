import asyncio
import os
import httpx
from dotenv import load_dotenv
import time
from bookdb import Database
from content import similarity_scores, pt, books

import numpy as np
import pandas as pd

# Загрузка переменных окружения из .env файла
load_dotenv()

db = Database('var/db.sqlite3')

book_by_title = {}
for book_name in pt.index:
    book_by_title[book_name] = db.get_book_by_title(book_name)

def get_index(name):
    return np.where(pt.index == name)[0][0]

def get_best(feedbacks):
    # Finding the index of the specific book, 'book_name', within the 'pt' pivot table's index
    rating = []
    f_names = [ get_book_name(f[0]) for f in feedbacks ]
    for book_name in pt.index:
        if book_name in f_names:
            rating.append((book_by_title[book_name], 0))
            continue
        c_r = 0
        total = 0
        total_r = 0
        items_applied = 0
        book_index = get_index(book_name)
        for f in feedbacks:
            f_name = get_book_name(f[0])
            f_index = get_index(f_name)

            print(similarity_scores[book_index][f_index])
            c_r = max(c_r, similarity_scores[book_index][f_index] * f[1] / 10)

            if similarity_scores[book_index][f_index] > 0.5:
                total += similarity_scores[book_index][f_index]
                total_r += abs(similarity_scores[book_index][f_index] * f[1] / 10)
                items_applied += 1
        if items_applied > 0 and total > 0:
            rating.append((book_by_title[book_name], (c_r * 10 + total_r * items_applied / total) / (10 + items_applied)))
        else:
            rating.append((book_by_title[book_name], c_r))

    # print(rating)

    return sorted(rating, key=lambda x: x[1], reverse=True)[0]
    

def add_record(uid, book_uid, grade) -> None:
    db.put_grade(uid, book_uid, grade)


def get_recomendation(uid) -> str:
    tmp = get_best(db.get_grades(uid))
    print(tmp)
    return tmp[0][0]


def get_book_name(book_uid) -> str:
    print(book_uid)
    rs = db.get_book(book_uid)
    if type(None) == type(rs):
      return None
    book_name = rs[1]
    return book_name


def restart_user(uid) -> None:
    db.del_grades(uid)
    db.del_last(uid)
