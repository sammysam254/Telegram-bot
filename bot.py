import os
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create Flask app (to keep Render service alive)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running via polling on Render!", 200

# Telegram bot setup
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am alive and running on polling 🚀")

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

def run_polling():
    print("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    # Run polling in background thread so Flask can run too
    threading.Thread(target=run_polling, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
