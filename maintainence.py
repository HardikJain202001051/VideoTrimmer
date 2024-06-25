
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from utis import Config
app = None
Bot = None


async def maintenance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot under maintenance 🧑‍🔧...we will let you know when when up and working.")

def main():
    # Builds the server side application for our telegram bot using the bot token
    global app
    app = ApplicationBuilder().token(Config.token).concurrent_updates(True).build()
    app.add_handler(MessageHandler(filters.TEXT, maintenance_handler))
    app.run_polling()

if __name__ == '__main__':
    main()
