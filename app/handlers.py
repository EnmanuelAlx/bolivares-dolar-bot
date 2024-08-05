from telegram.ext import Application, CommandHandler, ContextTypes
import traceback
from app.models import PriceCalculator
from app.scrapper import BCVScrapper


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log the error and send a telegram message to notify the developer."""

    logger.error("Exception while handling an update:", exc_info=context.error)

    update_str = (
        update.to_dict() if isinstance(update, Update) else str(update)
    )

    message = (
        "An exception was raised while handling an update\n" f"{update_str}"
    )

    # Finally, send the message

    await context.bot.send_message(text=message)


async def bcv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        scrapper = BCVScrapper()
        price = scrapper.get_dollar_price()
        calculator = PriceCalculator(currency_price=price)
        text_after_command = context.args
        rate_change = calculator.calculate_price(text_after_command)
        message = ""
        if len(context.args) > 1:
            sum_amounts = calculator.sum_amounts(text_after_command)
            message = f"La suma de tus montos es: {sum_amounts}$ \n"
        message += f"El precio del dolar es: {price} \nAl cambio sería: {rate_change} Bs"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(e)
