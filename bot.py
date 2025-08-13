import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

# Create Flask app
app = Flask(__name__)

# Create Telegram bot application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] /start command received from {update.effective_user.username}")
    await update.message.reply_text("Hello! I am alive and running on polling 🚀")

# General message handler (logs and replies)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    text = update.message.text
    print(f"[LOG] Message from {user}: {text}")
    await update.message.reply_text(f"You said: {text}")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Flask home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is running with polling!", 200

# Function to start Telegram bot polling in a separate thread
def run_polling():
    print("[LOG] Starting Telegram bot polling...")
    application.run_polling()

if __name__ == "__main__":
    # Start polling in a background thread
    threading.Thread(target=run_polling, daemon=True).start()

    # Start Flask app (for Render health check)
    app.run(host="0.0.0.0", port=PORT)
