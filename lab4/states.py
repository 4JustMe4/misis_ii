from aiogram.fsm.state import StatesGroup, State


class TranslationStates(StatesGroup):
    """
    Класс состояний для машины состояний бота.

    Атрибуты состояний:
    - waiting_for_genre: Ожидание выбора жанра.
    - waiting_for_author: Ожидание выбора автора.
    - waiting_for_wish: Ожидание пожелания.
    - waiting_for_addition: Ожидание ответа на запрос о дополнительной рекомендации.
    - waiting_for_continue: Ожидание ответа о продолжении работы с ботом.
    """

    waiting_for_genre: State = State()
    waiting_for_author: State = State()
    waiting_for_wish: State = State()
    waiting_for_addition: State = State()
    waiting_for_continue: State = State()
