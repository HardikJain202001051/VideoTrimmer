import asyncio

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler, Application
from utis import is_valid_youtube_link, Config, parse_timestamp
import uuid
import subprocess
import os
from pathlib import Path
from utis import find_file_with_prefix

dir_path = ''
user_state = {}
app = None
Bot = None

# Bot().send_video()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function has been registered as callback for /start command handler.
    update:contains all the information about the user query which made this callback execute
    """
    user_id = update.message.from_user.id
    if user_id not in Config.allowed_users:
        return
    user_state[user_id] = {
        "step": "link",
    }
    await update.message.reply_text(
        f'Hey {update.effective_user.first_name}, Please send link to the YouTube video and follow the steps')


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in Config.allowed_users:
        await update.message.reply_text("You do not have permission to access this bot.")
        return
    await update.message.reply_text("• You can directly send the YouTube video link and follow the steps to trim the "
                                    "video.\n• For longer clips consider creating multiple clips, each not more than 4 "
                                    "minutes or you might face error."
                                    "\n\n• Examples for valid timestamp format\n"
                                    " ◦ 1h 1m 1s => 1.1.1\n"
                                    " ◦ 1h 1s => 1.0.1\n"
                                    " ◦ 1s => 1\n"
                                    " ◦ 1m => 1.0\n"
                                    " ◦ 1h => 1.0.0\n"
                                    "")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in Config.allowed_users:
        await update.message.reply_text("You do not have permission to access this bot.")
        return
    text = update.message.text
    if user_state[user_id]['step'] == 'link':
        if not is_valid_youtube_link(text):
            await update.message.reply_text('Send a valid YouTube Video URL.')
        else:
            user_state[user_id]['step'] = 'start'
            user_state[user_id]['link'] = text
            await update.message.reply_text('Enter the start time\n\nExample -> 1h 20m 10s')

    elif user_state[user_id]['step'] == 'start':
        start = parse_timestamp(text)
        if start is not None:
            user_state[user_id]['start_time'] = start
            user_state[user_id]['step'] = 'end'
            await update.message.reply_text('Enter the end time')
        else:
            await update.message.reply_text("Send a valid timestamp or use /start command to start again. Use "
                                            "/help to find the valid timestamps")

    elif user_state[user_id]['step'] == 'end':
        end = parse_timestamp(text)
        if end is not None:

            start = user_state[user_id]['start_time']
            if start >= end:
                await update.message.reply_text("End time cannot be less than or equal to start time")
                return
            link = user_state[user_id]['link']
            user_state[user_id]['step'] = 'link'
            filename = str(uuid.uuid4())[:5]
            output_file = dir_path + filename
            wait_msg = await update.message.reply_text("⌛ Your request is in process...Please wait few minutes")
            cmd = f'yt-dlp  --format "mkv,mp4" --download-sections "*{start}-{end}" --force-keyframes-at-cuts -o {output_file} {link}'
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(proc.stdout)
            await wait_msg.edit_text("🎥 Your video has been downloaded...Uploading to Telegram ⬆️")
            output_file = dir_path + find_file_with_prefix(filename)
            retries = 3
            while retries:
                try:
                    await update.message.reply_video(video=output_file, read_timeout=600, write_timeout=600,
                                                     supports_streaming=True)
                    break
                except Exception as e:
                    retries -= 1
                    if retries == 0:
                        await update.message.reply_text("Encountered some error, please try again.")
                    await Bot.send_message(Config.owner,f"Encountered the following error\n{e}")
            file_path = Path(output_file)
            if file_path.exists():
                file_path.unlink()
                print("File deleted successfully.")
            else:
                print("File does not exist.")
        else:
            await update.message.reply_text('Send a valid timestamp or use /start command to start again.')

def set_commands(bot):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help information")
    ]

    # Set the commands for the bot
    loop = asyncio.get_event_loop()

    # Run the async function in the event loop
    loop.run_until_complete(bot.set_my_commands(commands))

def main():
    # Builds the server side application for our telegram bot using the bot token
    global app
    app = ApplicationBuilder().token(Config.token).concurrent_updates(True).build()

    """To respond to user queries we need to register handlers in the app. Handler will execute callback on receiving 
    the query. Different queries have different handlers. For eg, is user sends a command we need command handler The 
    below handler is for /start command where 'hello' function is registered as callback """
    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CommandHandler("help", help_))

    """This handler handles incoming messages. 
    filters.TEXT specifies that it will handle text messages only"""
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    """We can control the bot using 'app' directly or through the bot instance depending on the task
    For eg, to directly send a message to a user or group, we can use Bot.send_message(chat_id,text)"""
    global Bot
    Bot = app.bot
    set_commands(Bot)
    # Polling and webhooks both are allowed
    app.run_polling()


if __name__ == '__main__':
    Config.owner = Config.allowed_users[0]
    for user in Config.allowed_users:
        user_state[int(user)] = {'step': 'link'}
    dir_path = Config.dir_path
    main()
