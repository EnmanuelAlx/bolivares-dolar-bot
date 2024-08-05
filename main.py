import logging

from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler

from app.constants import TELEGRAM_TOKEN
from app.handlers import bcv, error_handler

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    commands = [
        BotCommand("bcv", "Obtener el precio del dólar y calcular el cambio")
    ]
    application.bot.set_my_commands(commands, language_code="es")
    application.add_handler(CommandHandler("bcv", bcv))

    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
