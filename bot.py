import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")  # Your web app link
PORT = int(os.getenv("PORT", 5000))

# Flask app
app = Flask(__name__)

# Telegram app
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Open Web App 🌐", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Tap below to open the app:", reply_markup=reply_markup)

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running on Render!", 200

# Start bot + Flask
if __name__ == "__main__":
    async def set_webhook():
        public_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
        await application.bot.set_webhook(public_url)
        print(f"Webhook set to {public_url}")

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=PORT)
