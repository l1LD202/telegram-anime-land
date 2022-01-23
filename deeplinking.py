from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)

# Enable logging
from telegram.utils import helpers

users = {}

def start(update: Update, context: CallbackContext) -> None:
    """Send a deep-linked URL when the command /start is issued."""
    bot = context.bot
    user_id = update.effective_user.id
    print(f'{user_id}')
    url = helpers.create_deep_linked_url(bot.username, f"join_{user_id}")
    text = "Feel free to tell your friends about it:\n\n" + url
    update.message.reply_text(text)

def deep_linked_level_1(update: Update, context: CallbackContext):
    print(update.message)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5050742606:AAEscBT-LUM94Mq1lN31bw-Vfl06aRb90Mg")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # More info on what deep linking actually is (read this first if it's unclear to you):
    # https://core.telegram.org/bots#deep-linking

    # Register a deep-linking handler
    dispatcher.add_handler(
        CommandHandler("start", deep_linked_level_1, Filters.regex("join_[0-9]{10}"))
    )

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()