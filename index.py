from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Foydalanuvchi bosqichlarini saqlash uchun
user_steps = {}

# Bosqichdagi matnlar
messages = {
    1: "Bu birinchi xabar",
    2: "Bu ikkinchi xabar",
    3: "Bu uchinchi xabar"
}

TOKEN = "BOT_TOKENINGIZNI_BU_YERGA_QO'YING"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_steps[user_id] = 1  # boshlang'ich bosqich
    await send_step_message(update, context, user_id)

async def send_step_message(update, context, user_id):
    step = user_steps[user_id]
    text = messages.get(step, "Boshqa xabar yo'q")
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(str(step), callback_data=str(step))]]
    )

    if hasattr(update, "callback_query") and update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=keyboard)
    elif hasattr(update, "message") and update.message:
        await update.message.reply_text(text, reply_markup=keyboard)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    step = user_steps.get(user_id, 1)

    # Faqat hozirgi tugma bosilganda keyingi bosqichga o'tkazish
    if query.data == str(step):
        user_steps[user_id] += 1
        await send_step_message(update, context, user_id)
    else:
        await query.message.reply_text("Avval oldingi bosqichni yakunlang!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

print("Bot ishga tushdi...")
app.run_polling()
