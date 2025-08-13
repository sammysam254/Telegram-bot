from flask import Flask
from telegram.ext import CommandHandler, Updater

app = Flask(__name__)

def start(update, context):
    update.message.reply_text("Hello!")

def start_bot():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    print("Bot started...")

# Run the bot once at startup
with app.app_context():
    start_bot()

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run()
