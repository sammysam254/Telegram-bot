import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")  # Example: https://your-app-name.onrender.com
WEB_APP_URL = os.getenv("WEB_APP_URL")  # Your Telegram Mini App URL
PORT = int(os.getenv("PORT", 5000))

# Create Flask app
app = Flask(__name__)

# Create Telegram application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Open Mini App", web_app={"url": WEB_APP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Tap below to open the Mini App:",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is running on Render!", 200

if __name__ == "__main__":
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(f"{RENDER_URL}/{BOT_TOKEN}")
        print(f"Webhook set to {RENDER_URL}/{BOT_TOKEN}")

    asyncio.run(set_webhook())

    # Start Flask app
    app.run(host="0.0.0.0", port=PORT)
