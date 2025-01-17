import asyncio
from aiogram import Bot, Dispatcher
from bot import router
import os
from aiogram.types import BotCommand
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена бота из переменной окружения
API_TG_BOT: str = os.getenv("TELEGRAM_TOKEN", "")

# Создание экземпляра бота с полученным токеном
bot: Bot = Bot(token=API_TG_BOT)

# Создание экземпляра диспетчера для бота
dp: Dispatcher = Dispatcher()

# Подключение маршрутизатора (router) для обработки команд и сообщений
dp.include_router(router)


async def set_bot_commands(bot: Bot) -> None:
    """
    Устанавливает начальные команды для бота, которые будут отображаться в меню команд.

    :param bot: Экземпляр бота, для которого нужно установить команды.

    :return: None. Функция выполняет асинхронное обновление команд в меню бота.
    """
    commands = [
        BotCommand(
            command="start", description="Запуск бота"
        ),  # Команда для запуска бота
        BotCommand(
            command="help", description="Получить помощь"
        ),  # Команда для получения помощи
        BotCommand(
            command="id", description="Получить свой id"
        ),  # Команда для получения id пользователя
        BotCommand(
            command="restart", description="Сбросить бота"
        ),  # Команда для получения id пользователя
    ]

    await bot.set_my_commands(commands)  # Устанавливаем команды в меню бота


async def main() -> None:
    """
    Основная функция для запуска бота.

    :return: None. Функция запускает бота и обрабатывает входящие сообщения.
    """
    await asyncio.sleep(1)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск главной асинхронной функции
    asyncio.run(main())
