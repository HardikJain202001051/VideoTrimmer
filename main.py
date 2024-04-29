import asyncio

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utis import is_valid_youtube_link, Config, parse_timestamp
import uuid
import subprocess
import os
from pathlib import Path
from utis import find_file_with_prefix

dir_path = ''
allowed_users = set()
user_state = {}


# Bot().send_video()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function has been registered as callback for /start command handler.
    update:contains all the information about the user query which made this callback execute
    """

    user_id = str(update.message.from_user.id)
    if user_id not in allowed_users:
        return
    await update.message.reply_text(
        f'Hey {update.effective_user.first_name}, Please send the link and follow the steps', disable_web_page_preview=True)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id not in allowed_users:
        await update.message.reply_text("You do not have permission to access this bot.")
    text = update.message.text
    if user_state[user_id]['step'] == 'link':
        if not is_valid_youtube_link(text):
            await update.message.reply_text('Send a valid YouTube Video URL.')
        else:
            user_state[user_id]['step'] = 'start'
            user_state[user_id]['link'] = text
            await update.message.reply_text('Enter the start time\n\nExample -> 1h 20m 10s')

    elif user_state[user_id]['step'] == 'start':
        user_state[user_id]['start_time'] = text
        user_state[user_id]['step'] = 'end'
        await update.message.reply_text('Enter the end time')


    elif user_state[user_id]['step'] == 'end':
        start = user_state[user_id]['start_time']
        end = text
        start,end = parse_timestamp(start), parse_timestamp(end)
        if not end or not start:
            await update.message.reply_text('Send a valid timestamp range')
        else:
            link = user_state[user_id]['link']
            user_state[user_id]['step'] = 'link'
            filename = str(uuid.uuid4())[:5]
            output_file = dir_path + filename
            cmd = f'yt-dlp  --format "mkv,mp4" --download-sections "*{start}-{end}" --force-keyframes-at-cuts -o {output_file} {link}'
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(proc.stdout)
            output_file = dir_path + find_file_with_prefix(filename)
            retries = 3
            while retries:
                try:
                    await update.message.reply_video(video=output_file, read_timeout=600, write_timeout=600,
                                                     supports_streaming=True)
                    break
                except TimeoutError:
                    break
                except Exception as e:
                    retries -= 1
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
    user_state = Config.user_state
    allowed_users = Config.allowed_users
    dir_path = Config.dir_path
    main()
