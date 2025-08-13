import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")  # Example: https://yourapp.onrender.com
PORT = int(os.getenv("PORT", 5000))

# Create Flask app
app = Flask(__name__)

# Create Telegram application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive on Render 🚀")

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
    # Set webhook before starting Flask
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(f"{RENDER_URL}/{BOT_TOKEN}")
        print(f"Webhook set to {RENDER_URL}/{BOT_TOKEN}")

    asyncio.run(set_webhook())

    # Start Flask app
    app.run(host="0.0.0.0", port=PORT)
