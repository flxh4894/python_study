import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


"""
    Base Telegram 
    텔레그램을 사용하기 위한 
"""
class BaseTelegram:
    def __init__(self, token) -> None:
        self.TOKEN = token
        pass

    def start_command(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )

    def help_command(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text("Help Message")    

    def echo_command(update: Update, context: CallbackContext) -> None:
        """Get user text and reply."""
        update.message.reply_text(update.message.text)
    
    def init(self):
        updater = Updater(self.TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("help", self.help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo_command))

        updater.start_polling()
        updater.idle()
        pass