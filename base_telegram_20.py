import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from dotenv import load_dotenv
import os
import word as w

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

reply_keyboard = [
    ["추가", "리스트", "제거"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

LIST = {}
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_markup=markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/start : start bot\n/help : help message")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if((message == w.ADD_DONE) and update.effective_user.id in LIST):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="등록 완료 되었습니다.", reply_markup=markup)
        del LIST[update.effective_user.id]
        return
    elif(update.effective_user.id in LIST):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="해당 물건검색중입니다 :: {}".format(message))
        return
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="기타 - /help 를 입력해서 사용 방법을 확인하세요.")
        return


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    LIST[update.effective_user.id] = True
    await update.message.reply_text("가격변동 알리미 🔔\n검색어를 상세하게 입력해주세요 🔍\n최대 15개의 상품이 조회됩니다.")
    return CHOOSING



async def echo1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("상품을 검색중입니다. 잠시만 기다려주세요 🔍")
    reply_keyboard = [
        ["등록완료"],
        ["아이패드"],
        ["아이폰"],
    ]
    items = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("알림 받기 원하는 상품을 클릭해주세요 🔔\n여러개 선택이 가능하며, 모두 선택 후 완료 버튼을 눌러주세요 😊", reply_markup=items)
    return TYPING_CHOICE

async def echo2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    await update.message.reply_text("선택상품 {}".format(message))

async def echo3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Done!", reply_markup=markup)
    return ConversationHandler.END


async def echo4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("444444")


async def echo5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("error")

if __name__ == "__main__":
    load_dotenv()
    application = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    # application.add_handler(CommandHandler('add', add_command))
    # application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))d


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_command)],
        states={
            CHOOSING: [
                MessageHandler(filters.TEXT, echo1)
                # MessageHandler(
                #     filters.Regex("^(Age|Favourite colour|Number of siblings)$"), echo1
                # ),
                # MessageHandler(filters.Regex("^Something else...$"), echo2),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.Regex("^({})$".format(w.ADD_DONE)), echo3
                ),
                MessageHandler(filters.TEXT, echo2),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    echo4,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), echo5)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.COMMAND, unknown))


    application.run_polling()

    application.bot