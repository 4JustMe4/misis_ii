from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api import get_recomendation_from_rugpt, get_recomendation_from_llama
from constants import GENRES, AUTHORS
from keyboards import (
    get_genre_keyboard,
    get_author_keyboard,
    get_addition_keyboard,
    get_continue_keyboard,
    get_start_help_keyboard,
)
from states import TranslationStates
import time

router: Router = Router()


def escape_md(text: str) -> str:
    """Экранирует специальные символы Markdown."""
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /start."""
    await message.answer(
        "Привет! Я твой помощник по выбору книги. Выбери какой жанр ты хочет бы почитать или впиши свой:",
        reply_markup=get_genre_keyboard(),
    )
    await state.set_state(TranslationStates.waiting_for_genre)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обрабатывает команду /help."""
    help_text = (
        "Я могу помочь с рекомендацией книги.\n\n"
        "Команды:\n"
        "/start — начать работу с ботом.\n"
        "/help — показать эту справку.\n"
        "/id — посмотреть свой id.\n\n"
        "Как пользоваться ботом:\n"
        "1. Выберите жанр или введите свой.\n"
        "2. Выберите автора или введите своего.\n"
        "3. Добавьте произвольное пожелание к книге.\n"
        "4. Получите рекомендацию.\n\n"
        "Можно получить вторую рекомендацию от другой модели!"
    )
    await message.answer(help_text, reply_markup=get_start_help_keyboard())


@router.message(TranslationStates.waiting_for_genre)
async def choose_genre(message: Message, state: FSMContext) -> None:
    """Обрабатывает выбор жанра."""
    genre = message.text
    if genre.lower() in GENRES:
        await state.update_data(genre=genre)
    else:
        await state.update_data(genre=genre)
        await message.answer("Буду знать этот жанр!")

    await message.answer(
        "Выбери автора или впиши своего:", reply_markup=get_author_keyboard()
    )
    await state.set_state(TranslationStates.waiting_for_author)


@router.message(TranslationStates.waiting_for_author)
async def choose_author(message: Message, state: FSMContext) -> None:
    """Обрабатывает выбор автора."""
    author = message.text
    if author.lower() in AUTHORS:
        await state.update_data(author=author)
    else:
        await state.update_data(author=author)
        print(author)
        print(AUTHORS)
        print(AUTHORS[2] == author)
        for i in range(len(author)):
            print(author[i], AUTHORS[2][i], AUTHORS[2][i] == author[i])
        await message.answer("Буду знать этого автора!")

    await message.answer("Добавь пожелание к книге")
    await state.set_state(TranslationStates.waiting_for_wish)


@router.message(TranslationStates.waiting_for_wish)
async def add_wish(message: Message, state: FSMContext) -> None:
    """Обрабатывает все пожелания и отправляет в API RuGPT."""
    data = await state.get_data()
    genre = data["genre"]
    author = data["author"]
    wish = message.text

    await state.update_data(wish=wish)

    # Время выполнения запроса
    rugpt_recomendation = await get_recomendation_from_rugpt(genre, author, wish)

    # Ответ с рекомендацией
    escaped_recomendation = escape_md(rugpt_recomendation)
    await message.answer(
        f"*Рекомендация от ruGPT*:\n{escaped_recomendation}\n", parse_mode="MarkdownV2"
    )

    # Спрашиваем, хочет ли пользователь получить рекомендацию от другого api
    await message.answer(
        "Хочешь сравнить с рекомендацией от другого API?",
        reply_markup=get_addition_keyboard(),
    )
    await state.set_state(TranslationStates.waiting_for_addition)


@router.message(TranslationStates.waiting_for_addition)
async def compare_translations(message: Message, state: FSMContext) -> None:
    """Обрабатывает запрос на дополнительную рекомендацию."""
    if message.text.lower() == "да":
        data = await state.get_data()
        genre = data["genre"]
        author = data["author"]
        wish = data["wish"]

        llama_recomendation = await get_recomendation_from_llama(genre, author, wish)
        escaped_recomendation = escape_md(llama_recomendation)
        await message.answer(
            f"*Рекомендация от LLaMA*:\n{escaped_recomendation}",
            parse_mode="MarkdownV2",
        )

    await message.answer(
        "Хочешь получить еще рекомендаций?", reply_markup=get_continue_keyboard()
    )
    await state.set_state(TranslationStates.waiting_for_continue)


@router.message(TranslationStates.waiting_for_continue)
async def continue_translation(message: Message, state: FSMContext) -> None:
    """Обрабатывает запрос на продолжение работы."""
    if message.text.lower() == "да":
        await message.answer(
            "Выбери жанр или впиши свой:", reply_markup=get_genre_keyboard()
        )
        await state.set_state(TranslationStates.waiting_for_genre)
    else:
        await message.answer(
            "Спасибо, что воспользовались ботом! Вы можете начать заново или посмотреть справку.",
            reply_markup=get_start_help_keyboard(),
        )
        await state.clear()


@router.message(Command("id"))
async def show_user_id(message: Message) -> None:
    """Обрабатывает команду /ID."""
    await message.answer(f"Твой ID: {message.from_user.id}")
