import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


"""
    Base Telegram 
    텔레그램을 사용하기 위한 Class
"""
class BaseTelegram:
    def __init__(self, token: str) -> None:
        self.TOKEN = token
        self.init()
        pass

    def start_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        keyboard = [
                [
                    InlineKeyboardButton("Option 1", callback_data="1"),
                    InlineKeyboardButton("Option 2", callback_data="2"),
                ],
                [InlineKeyboardButton("Option 3", callback_data="3")],
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Please choose:", reply_markup=reply_markup)


    def start_option(self, update: Update, context: CallbackContext) -> None:
        """Start button option"""
        q = update.callback_query
        q.answer()
        logger.debug(q.data)
        q.edit_message_text(text=f"Selected option: {q.data}")


    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text("Help Message")    


    def echo_command(self, update: Update, context: CallbackContext) -> None:
        """Get user text and reply."""

        logger.info("{} :: {}".format(update.effective_user.full_name,update.message.text))
        update.message.reply_text(update.message.text)
    

    def init(self):
        """init function"""
        updater = Updater(self.TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CallbackQueryHandler(self.start_option))
        dispatcher.add_handler(CommandHandler("help", self.help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo_command))

        updater.start_polling()
        updater.idle()
        pass