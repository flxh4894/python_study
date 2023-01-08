from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import word as w
from home_markup import markup, goHome

# /add 관련 state 설정
SEARCH_ITEM, APPLY_ITEM = range(2)

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("가격변동 알리미 🔔\n검색어를 상세하게 입력해주세요 🔍\n최대 15개의 상품이 조회됩니다.")
    return SEARCH_ITEM


# 아이템 검색
async def search_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("상품을 검색중입니다. 잠시만 기다려주세요 🔍")
    # 검색이 됐다고 가정을 하는 리스트
    data_list = [
        ["등록완료"],
        ["아이패드 프로 12.9 5세대 M1^_^v_"],
        ["아이패드 프로 11인치 3세대 M1^_^v_"],
        ["아이패드 거치대^_^v_"],
        ["아이패드 미니 6세대 64Gb 와이파이^_^v_"],
        ["에러발생용 미니 6세대 64Gb 와이파이"]
    ]
    reply_list = ReplyKeyboardMarkup(data_list, one_time_keyboard=False)
    await update.message.reply_text("알림 받기 원하는 상품을 클릭해주세요 🔔\n여러개 선택이 가능하며, 모두 선택 후 완료 버튼을 눌러주세요 😊", reply_markup=reply_list)
    return APPLY_ITEM


# 아이템 등록
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if(w.PARSER in message):
        try:
            await update.message.reply_text("선택상품 등록 완료 :: {}".format(message))
        except:
            await update.message.reply_text("등록중 오류가 발생했습니다 🚫\n🔽 키보드 왼쪽 메뉴를 이용해주세요", reply_markup=markup)
            return ConversationHandler.END
    else:
        await goHome(update=update)
        return ConversationHandler.END


async def done_add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await goHome(update=update)
    return ConversationHandler.END


async def error_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await goHome(update=update)
    return ConversationHandler.END


# 핸들러 설정
conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_command)],
        states={
            # 아이템 검색
            SEARCH_ITEM: [
                MessageHandler(filters.TEXT, search_list)
            ],
            # 아이템 등록
            APPLY_ITEM: [
                # 1. 등록완료
                MessageHandler(filters.Regex("^({})$".format(w.ADD_DONE)), done_add_item ),
                # 2. 계속등록
                MessageHandler(filters.TEXT & ~(filters.COMMAND), add_item)
            ]
        },
        fallbacks=[MessageHandler(filters.TEXT, error_task)],
    )