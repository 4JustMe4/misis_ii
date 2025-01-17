from aiogram.fsm.state import StatesGroup, State


class TranslationStates(StatesGroup):
    """
    Класс состояний для машины состояний бота.

    Атрибуты состояний:
    - waiting_for_init_book: Ожидание начала работы.
    - waiting_for_feedback: Ожидание фидбека
    - waiting_for_restart: Удаление информации о пользователе
    """

    waiting_for_init_book: State = State()
    waiting_for_feedback: State = State()
    waiting_for_restart: State = State()
