import asyncio
from process_video import trim_video
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utis import is_valid_youtube_link
from process_link import get_available_qualities, download_video
import uuid

dir_path = 'C:\\Users\\hardik\\PycharmProjects\\TeleGramBot\\TrimmedVideoDownloaded\\'
# Bot().send_video()
state = {5343698850: {
    'step': None,
    'start_timestamp': None,
    'end_timestamp': None,
    'link': None,
    'filename':None
}}
pattern = r'^download\|\d+$'


async def trim_and_send(user_id: int, chat_id: int):
    start = state[user_id]['start_timestamp']
    end = state[user_id]['end_timestamp']
    filename = await state[user_id]['filename']
    trim_video(filename, start, end)
    state[user_id]['step'] = None
    await Bot.send_video(chat_id, video=dir_path+'trimmed-'+filename)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in state.keys():
        return
    text = update.message.text
    if state[user_id]['step'] is None:
        if not is_valid_youtube_link(text):
            await update.message.reply_text('Send a valid YouTube Video URL.')
        else:
            state[user_id]['filename'] = asyncio.create_task(download_video(youtube_link=text,filename=str(uuid.uuid4())[:8]+'.mp4'))
            state[user_id]['step'] = 'start_time'
            await update.message.reply_text('Enter the start time')
            # videos = get_available_qualities(text)
            # buttons = []
            # for video in videos:
            #     if video.resolution:
            #         buttons.append([InlineKeyboardButton(text=f"⬇️{video.resolution}, ~{video.filesize_mb:.2f}MB",
            #                                              callback_data=f'download|{video.itag}')])
            # inline_buttons = InlineKeyboardMarkup(buttons)
            # # print(inline_buttons)
            # state[user_id]['link'] = text
            # await update.message.reply_text(text='Select the desired video quality.', reply_markup=inline_buttons)
    elif state[user_id]['step'] == 'start_time':
        state[user_id]['start_timestamp'] = int(update.message.text)
        await update.message.reply_text('Enter the end time')
        state[user_id]['step'] = 'end_time'
    elif state[user_id]['step'] == 'end_time':
        state[user_id]['start_timestamp'] = int(update.message.text)
        chat_id = update.message.chat_id
        asyncio.create_task(trim_and_send(user_id, chat_id))

#
# async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     data = update.callback_query.data
#     itag = data.split('|')[1]
#     youtube_link = state[user_id]['link']
#     task = asyncio.create_task(download_video(youtube_link, itag))
#     state[user_id]['path'] = task
#     await update.callback_query.message.delete()
#     print(state)
#     await update.callback_query.message.reply_text('Enter the start time')


app = ApplicationBuilder().token("5944818109:AAGQCaZtNDPwWKiW57EeNie1bCLhUfLrJO0").build()

app.add_handler(CommandHandler("start", hello))
app.add_handler(MessageHandler(filters.TEXT, handle_messages))
# app.add_handler(CallbackQueryHandler(callback=get_video, pattern=pattern))
Bot = app.bot
app.run_polling()
