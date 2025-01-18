#!/usr/bin/env python3
import sqlite3,csv
import sys,json
import traceback

#Table grades {
#id INTEGER [primary key, unique, not null]
#telegram_uid INTEGER
#uid VARCHAR [primary key, unique, not null, note: 'mephi | misis']
#name TEXT [not null, note: 'ex. НИТУ МИСИС']
#}
#
#Table lastbooks {
#user_id INTEGER [primary key, unique, not null]
#book_id INTEGER [primary key, unique, not null]
#}

#id INTEGER NOT NULL AUTOINCREMENT,
TRANSACTION_INIT = '''
CREATE TABLE IF NOT EXISTS bookgrades (
    user_tid INTEGER NOT NULL,
    book_uid VARCHAR NOT NULL,
    grade REAL, 
    PRIMARY KEY (user_tid, book_uid)
);

CREATE TABLE IF NOT EXISTS lastbooks (
    user_tid INTEGER PRIMARY KEY,
    book_uid VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    uid VARCHAR PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    author TEXT NOT NULL
);
'''

TRANSACTION_INSERT_BOOKGRADE = '''
INSERT INTO bookgrades (user_tid, book_uid, grade)
VALUES (?, ?, ?)
ON CONFLICT (user_tid, book_uid) DO UPDATE SET 
    grade = excluded.grade;
'''

TRANSACTION_INSERT_LASTBOOK = '''
INSERT INTO lastbooks (user_tid, book_uid)
VALUES (?, ?)
ON CONFLICT (user_tid) DO UPDATE SET 
    book_uid = excluded.book_uid;
'''

TRANSACTION_SELECT_BOOKGRADES = '''
SELECT 
    bg.book_uid AS book_uid,
    bg.grade AS grade
FROM bookgrades bg
WHERE bg.user_tid = ?;
'''

TRANSACTION_SELECT_LASTBOOK = '''
SELECT
    lb.book_uid AS book_uid
FROM lastbooks lb
WHERE lb.user_tid = ?;
'''

TRANSACTION_DELETE_BOOKGRADES = '''
DELETE FROM bookgrades
WHERE user_tid = ?;
'''

TRANSACTION_DELETE_LASTBOOK = '''
DELETE FROM lastbooks
WHERE user_tid = ?;
'''

TRANSACTION_INSERT_BOOK = '''
INSERT INTO books (uid, name, author)
VALUES (?, ?, ?)
ON CONFLICT (uid) DO UPDATE SET 
    name = excluded.name,
    author = excluded.author;
'''
TRANSACTION_SELECT_BOOK = '''
SELECT
    bk.uid AS uid,
    bk.name AS name,
    bk.author AS author
FROM books bk
WHERE bk.uid = ?;
'''


class Database:
  def __init__(self, db_path = 'var/db.sqlite3'):
    self.conn = sqlite3.connect(db_path)
    self.cur = self.conn.cursor()
    self.cur.executescript(TRANSACTION_INIT)
  def __del__(self):
    self.cur.close()
    self.conn.close()

  def put_grade(self,user_tid, book_uid, grade):
    self.cur.execute(TRANSACTION_INSERT_BOOKGRADE, (user_tid, book_uid, grade))
    self.conn.commit()

  def get_grades(self, user_tid):
    self.cur.execute(TRANSACTION_SELECT_BOOKGRADES, (user_tid,))
    rows = self.cur.fetchall()
    return rows

  def del_grades(self, user_tid):
    self.cur.execute(TRANSACTION_DELETE_BOOKGRADES, (user_tid,))

  def set_last(self, user_tid, book_uid): 
    self.cur.execute(TRANSACTION_INSERT_LASTBOOK, (user_tid, book_uid))
    self.conn.commit()

  def get_last(self, user_tid):
    self.cur.execute(TRANSACTION_SELECT_LASTBOOK, (user_tid,))
    items = self.cur.fetchall()
    if len(items) == 0:
      return None
    return items[0][0]

  def del_last(self, user_tid):
    self.cur.execute(TRANSACTION_DELETE_LASTBOOK, (user_tid,))

  def insert_books(self,csv_path='var/Books.csv'):
    with open(csv_path, 'r') as file_obj:
      csv_reader = csv.reader(file_obj)
      
      #ISBN,Book-Title,Book-Author,Year-Of-Publication,Publisher,Image-URL-S,Image-URL-M,Image-URL-L
      for row in csv_reader:
        uid,name,author,year,publisher = row[0:5]
        #print(uid,name,author,year,publisher)
        self.cur.execute(TRANSACTION_INSERT_BOOK, (uid,name,author,))
      self.conn.commit()

  def get_book(self, book_uid):
    self.cur.execute(TRANSACTION_SELECT_BOOK, (book_uid,))
    items = self.cur.fetchall()
    if len(items) == 0:
      return None
    return items[0]


if __name__ == "__main__":
  db = Database()
  db.insert_books()

  db.put_grade(1, 2, 3.6)
  db.put_grade(1, 3, 2.7)
  db.put_grade(1, 4, 9.2)
  db.put_grade(2, 3, 5.1)
  db.put_grade(2, 5, 4.9)
      
  print(db.get_grades(1)) # -> [(2, 3.6), (3, 2.7), (4, 9.2)]
  print(db.get_grades(2)) # -> [(3, 5.1), (5, 4.9)]

  db.del_grades(1)
  db.del_grades(2)

  print(db.get_grades(1)) # -> []

  db.set_last(1,4)

  print(db.get_last(1)) # -> 4
  print(db.get_last(2)) # -> None

  db.del_last(1)

  print(db.get_last(1)) # -> None

  print(db.get_book('034543191X'))
  print(db.get_book('0679423079'))
  print(db.get_book('0679'))

