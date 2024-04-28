from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton,Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utis import is_valid_youtube_link
import uuid
import subprocess
import json

"""
token: Unique ID of telegram Bot
dir_path:  dir where downloaded videos will be stored
"""
with open('config.json') as f:
    config = json.load(f)
    dir_path = config['videos_path']
    print(dir_path)
    token = config['token']

"""
state contains Unique IDs of tg users as keys and their info as value
"""
state = {5343698850: {
    'step': None,
    'start_timestamp': None,
    'end_timestamp': None,
    'link': None,
    'filename':None
}}




async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function has been registered as callback for /start command handler.
    update:contains all the information about the user query which made this callback execute
    """
    user_id = update.message.from_user.id
    if user_id not in state.keys():
        return
    state[user_id] = {
        'step': None,
        'start_timestamp': None,
        'end_timestamp': None,
        'video_link': None, }
    await update.message.reply_text(
        f'Hey {update.effective_user.first_name}, Please send the link of YouTube Video you want to trim')


def check_timestamp(timestamp):
    timestamp = timestamp.split('.')
    if len(timestamp) > 3:
        return None
    for i in timestamp:
        if len(i) > 2 or not i.isdigit():
            return None
    return ':'.join(timestamp)

def get_timestamp(text):
    if len(text)<3:
        start = 0
    else:
        start = check_timestamp(text[1])
    end = check_timestamp(text[-1])
    return start,end


import os


def find_file_with_prefix( prefix):
    # Get list of files in the directory
    files = os.listdir(dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]

    return matching_files[0]




async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in state.keys():
        return
    text = update.message.text.split(' ')
    link = text[0]
    if state[user_id]['step'] is None:
        if not is_valid_youtube_link(text[0]):
            await update.message.reply_text('Send a valid YouTube Video URL.')
        else:
            start,end = get_timestamp(text)
            if not end:
                await update.message.reply_text('Send a valid timestamp range')
            else:
                filename = str(uuid.uuid4())[:5]
                output_file = dir_path+filename
                cmd = f'yt-dlp --download-sections "*{start}-{end}" --force-keyframes-at-cuts -o {output_file} {link}'
                print(cmd)
                subprocess.run(cmd)
                output_file = dir_path + find_file_with_prefix(filename)
                print(output_file)
                await update.message.reply_video(video=output_file,read_timeout=600,write_timeout=600)

                from pathlib import Path
                file_path = Path(output_file)
                if file_path.exists():
                    file_path.unlink()
                    print("File deleted successfully.")
                else:
                    print("File does not exist.")


# Builds the server side application for our telegram bot using the bot token
app = ApplicationBuilder().token(token).build()

"""
To respond to user queries we need to register handlers in the app. Handler will execute callback on recieving the query.
Different queries have different handlers.
For eg, is user sends a command we need command handler
The below handler is for /start command where 'hello' function is registered as callback
"""
app.add_handler(CommandHandler("start", hello))


"""
This handler handles incoming messages. 
filters.TEXT specifies that it will handle text messages only
"""
app.add_handler(MessageHandler(filters.TEXT, handle_messages))


"""
Below handler handles inline button clicks. 
"""
# pattern = r'^download\|\d+$'
# app.add_handler(CallbackQueryHandler(callback=get_video, pattern=pattern))

"""
We can control the bot using 'app' directly or through the bot instance depending on the task
For eg, to directly send a message to a user or group, we can use Bot.send_message(chat_id,text)
"""
Bot = app.bot


# Polling and webhooks both are allowed
app.run_polling()
