import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA = {}

def profit(update: Update, context: CallbackContext):
    try:
        buy = float(context.args[0])
        sell = float(context.args[1])
        p = sell - buy
        pct = (p / buy) * 100 if buy else 0
        today = date.today().isoformat()
        DATA.setdefault(today, []).append(p)
        update.message.reply_text(f"✅ الربح: {p:.2f} دج\n📊 النسبة: {pct:.2f}%")
    except:
        update.message.reply_text("استعمل: /ربح سعر_الشراء سعر_البيع")

def total(update: Update, context: CallbackContext):
    today = date.today().isoformat()
    grand = sum(sum(v) for v in DATA.values())
    today_sum = sum(DATA.get(today, []))
    update.message.reply_text(f"📅 الربح اليوم ({today}): {today_sum:.2f} دج\n🧾 الكلي: {grand:.2f} دج")

def reset(update: Update, context: CallbackContext):
    DATA.clear()
    update.message.reply_text("🔄 تم إعادة ضبط البيانات!")

def main():
    token = os.getenv("BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("ربح", profit))
    dp.add_handler(CommandHandler("مجموع", total))
    dp.add_handler(CommandHandler("إعادة", reset))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
