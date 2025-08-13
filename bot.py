import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")  # Example: https://yourapp.onrender.com
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running on Render.")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!", 200

def set_webhook():
    url = f"{RENDER_URL}/{BOT_TOKEN}"
    application.bot.set_webhook(url)

if __name__ == "__main__":
    # Set webhook before starting Flask server
    with application.bot:
        set_webhook()
    app.run(host="0.0.0.0", port=PORT)
