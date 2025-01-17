from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants import BOOKS


def get_init_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора книги.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=book) for book in BOOKS]],
        resize_keyboard=True,
    )

def get_empty_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт пустую клавиатуру.
    """
    return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)


def get_grade_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для оценки книги.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=str(grade)) for grade in range(11)]],
        resize_keyboard=True,
    )


def get_start_help_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора, хочет ли пользователь продолжить работу с ботом.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/start"),
                KeyboardButton(text="/help"),
                KeyboardButton(text="/id"),
            ]
        ],
        resize_keyboard=True,
    )
