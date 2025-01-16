from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants import GENRES, AUTHORS


def get_genre_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора жанра.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang.capitalize()) for lang in GENRES]],
        resize_keyboard=True,
    )


def get_author_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора автора.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang.capitalize()) for lang in AUTHORS]],
        resize_keyboard=True,
    )


def get_addition_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора, хочет ли пользователь получить рекомендацию от другой модели.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
        resize_keyboard=True,
    )


def get_continue_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора, хочет ли пользователь продолжить работу с ботом.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
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
