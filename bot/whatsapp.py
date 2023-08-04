from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,InlineQueryResultArticle, InputTextMessageContent ,InlineQueryResultDocument 
from telegram.ext import  CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes , InlineQueryHandler

async def whatsapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton('Fouad Mods', callback_data='fouad')],
        [InlineKeyboardButton('Sam Mods', callback_data='sam')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select a WhatsApp mod:', reply_markup=reply_markup)
