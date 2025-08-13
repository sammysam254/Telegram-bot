import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))
RENDER_URL = os.getenv("RENDER_URL")  # e.g. https://yourapp.onrender.com

app = Flask(__name__)

# Create the bot application
application = Application.builder().token(TOKEN).build()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am alive and running on Render!")

application.add_handler(CommandHandler("start", start))

# Flask route for Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

# Start Flask server and set webhook when app starts
@app.before_first_request
def set_webhook():
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    application.bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
