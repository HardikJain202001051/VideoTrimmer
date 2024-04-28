from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utis import is_valid_youtube_link, Config,get_timestamp
import uuid
import subprocess
import os
from pathlib import Path

dir_path = ''
allowed_users = []


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function has been registered as callback for /start command handler.
    update:contains all the information about the user query which made this callback execute
    """
    user_id = update.message.from_user.id
    if user_id not in allowed_users:
        return
    await update.message.reply_text(
        f'Hey {update.effective_user.first_name}, Please send the link of YouTube Video you want to trim')


def find_file_with_prefix(prefix):
    # Get list of files in the directory
    files = os.listdir(dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]
    return matching_files[0]


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in allowed_users:
        return
    text = update.message.text.split(' ')
    link = text[0]
    if not is_valid_youtube_link(text[0]):
        await update.message.reply_text('Send a valid YouTube Video URL.')
    else:
        start, end = get_timestamp(text)
        if not end:
            await update.message.reply_text('Send a valid timestamp range')
        else:
            filename = str(uuid.uuid4())[:5]
            output_file = dir_path + filename
            cmd = f'yt-dlp --download-sections "*{start}-{end}" --force-keyframes-at-cuts -o {output_file} {link}'
            print(cmd)
            subprocess.run(cmd)
            output_file = dir_path + find_file_with_prefix(filename)
            print(output_file)
            try:
                await update.message.reply_video(video=output_file, read_timeout=600, write_timeout=600)
            except Exception as e:
                await update.message.reply_text(str(e))
            file_path = Path(output_file)
            if file_path.exists():
                file_path.unlink()
                print("File deleted successfully.")
            else:
                print("File does not exist.")


# state contains Unique IDs of tg users as keys and their info as value
def main():
    # Builds the server side application for our telegram bot using the bot token
    app = ApplicationBuilder().token(Config.token).build()

    """To respond to user queries we need to register handlers in the app. Handler will execute callback on receiving 
    the query. Different queries have different handlers. For eg, is user sends a command we need command handler The 
    below handler is for /start command where 'hello' function is registered as callback """
    app.add_handler(CommandHandler("start", hello))

    """This handler handles incoming messages. 
    filters.TEXT specifies that it will handle text messages only"""
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    """We can control the bot using 'app' directly or through the bot instance depending on the task
    For eg, to directly send a message to a user or group, we can use Bot.send_message(chat_id,text)"""
    Bot = app.bot

    # Polling and webhooks both are allowed
    app.run_polling()

if __name__ == '__main__':

    allowed_users = Config.allowed_users
    dir_path = Config.dir_path
    main()