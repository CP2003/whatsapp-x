import os
from telegram import Bot , Update, InlineKeyboardMarkup, InlineKeyboardButton ,InlineQueryResultArticle, InputTextMessageContent ,InlineQueryResultDocument 
from telegram.ext import   ContextTypes 
import telegram.error 
BOT_USERNAME = os.environ.get('BOT_USERNAME')

async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []

    try:
        if 'w' in query:
            # First result: Fouad Mod Whatsapp
            fouad_button = InlineKeyboardButton('Fouad Mod Whatsapp', url=f'https://t.me/{BOT_USERNAME}?start=send_fouad')
            # Second result: Sam Mods Whatsapp
            sam_button = InlineKeyboardButton('Sam Mods Whatsapp', url=f'https://t.me/{BOT_USERNAME}?start=send_sam')

            reply_markup = InlineKeyboardMarkup([[fouad_button], [sam_button]])

            # Add the results to the list
            results.append(
                InlineQueryResultArticle(
                    id='1',
                    title='Whatsapp Mod Apks',
                    input_message_content=InputTextMessageContent(
                        message_text='Please select a WhatsApp mod:'
                    ),
                    description='Download Fouad Mod Whatsapp APK files',
                    thumb_url='https://i.ibb.co/YL52HVZ/photo-2023-08-05-06-37-35.jpg', 
                    reply_markup=reply_markup
                )
            )

    except telegram.error.BadRequest:
        pass  # Ignore the "Query is too old" error

    await update.inline_query.answer(results, cache_time=0)
