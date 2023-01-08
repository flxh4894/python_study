from telegram import ReplyKeyboardMarkup, Update


reply_keyboard = [
    ["추가", "리스트", "제거"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# Home 이동시 메뉴 변경 설정
async def goHome(update: Update):
    await update.message.reply_text("🔔 쿠팡 가격변동 알리미\n🔽 키보드 왼쪽 메뉴를 이용해주세요", reply_markup=markup)