from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api import add_record, get_recomendation, get_book_name, restart_user
from constants import BOOKS_LOWERED_UID
from keyboards import (
    get_init_keyboard,
    get_empty_keyboard,
    get_grade_keyboard,
    get_start_help_keyboard,
)
from states import TranslationStates
import time

router: Router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /start."""
    await message.answer(
        "Привет! Я твой помощник по выбору книги. Выбери лучшую по твоему мнению книгу",
        reply_markup=get_init_keyboard(),
    )
    await state.set_state(TranslationStates.waiting_for_init_book)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обрабатывает команду /help."""
    help_text = (
        "Я могу помочь с рекомендацией книги.\n\n"
        "Команды:\n"
        "/start — начать работу с ботом.\n"
        "/help — показать эту справку.\n"
        "/restart — перезапустить бота.\n"
        "/id — посмотреть свой id.\n\n"
        "Для начала работы напиши команду /start"
    )
    await message.answer(help_text, reply_markup=get_start_help_keyboard())


@router.message(Command("restart"))
async def cmd_restart(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /delete_profile."""
    restart_user(message.from_user.id)
    await message.answer(
        "До новых встреч!",
        reply_markup=get_empty_keyboard(),
    )
    await state.set_state(TranslationStates.waiting_for_restart)


@router.message(TranslationStates.waiting_for_init_book)
async def init_book(message: Message, state: FSMContext) -> None:
    book = message.text.lower()
    if book.lower() in BOOKS_LOWERED_UID:
        await state.update_data(book_uid=BOOKS_LOWERED_UID[book])
        await message.answer("Отлично! А как ты оценишь эту книгу?", reply_markup=get_grade_keyboard())
        await state.set_state(TranslationStates.waiting_for_feedback)
    else:
        await message.answer("К сожалению я не понял твой ответ. Повтори пожалуйста", reply_markup=get_init_keyboard())
        await state.set_state(TranslationStates.waiting_for_init_book)


@router.message(TranslationStates.waiting_for_feedback)
async def get_feedback(message: Message, state: FSMContext) -> None:
    grade = message.text
    try:
        grade = float(grade)
        await message.answer(f"Отлично! Я понял твою оценку {grade}")

        data = await state.get_data()
        uid = message.from_user.id
        add_record(uid, data["book_uid"], grade)

        new_book_uid = get_recomendation(uid)
        new_book_name = get_book_name(new_book_uid)

        await state.update_data(book_uid=new_book_uid)

        await message.answer(f"Тогда я порекомендую тебе {new_book_name}. Как ты оценишь ее?", reply_markup=get_grade_keyboard())
        await state.set_state(TranslationStates.waiting_for_feedback)

    except ValueError:
        await message.answer(f"Я не смог распознать твою оценку. Повтори ее пожалуйста.", reply_markup=get_grade_keyboard())
        await state.set_state(TranslationStates.waiting_for_feedback)


@router.message(TranslationStates.waiting_for_restart)
async def get_restart(message: Message, state: FSMContext) -> None:
    await message.answer(f"Ты вернулся! Напиши команду /start, чтобы начать!")
    await state.set_state(TranslationStates.waiting_for_restart)
    

@router.message(Command("id"))
async def show_user_id(message: Message) -> None:
    """Обрабатывает команду /ID."""
    await message.answer(f"Твой ID: {message.from_user.id}")
