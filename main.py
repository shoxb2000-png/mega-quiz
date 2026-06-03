import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = 8149451732
DB_NAME = "bot_data.db"

# Baza bilan ishlash
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, is_vip INTEGER, is_banned INTEGER, last_post TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings 
                      (id INTEGER PRIMARY KEY, post_limit INTEGER, is_blocked INTEGER)''')
    conn.commit()
    conn.close()

# Botni ishga tushirish qismi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Baza tekshiruvi va foydalanuvchini qo'shish
    await update.message.reply_text("Salom! Ish e'lonlari botiga xush kelibsiz.")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    keyboard = [
        [InlineKeyboardButton("Limitni o'zgartirish", callback_data='set_limit')],
        [InlineKeyboardButton("Foydalanuvchini bloklash", callback_data='ban_user')]
    ]
    await update.message.reply_text("Admin boshqaruv paneli:", reply_markup=InlineKeyboardMarkup(keyboard))

# Botni yurgizish
if __name__ == '__main__':
    init_db()
    application = Application.builder().token("8851319229:AAETKwNyvteBWO56HRx3PqeXsC0iIkpZW4A").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.run_polling()
