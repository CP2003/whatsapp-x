import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ContextTypes
import telegram.error ,asyncio, time

fmmods_whatsapp_link = os.environ.get('fmmods_whatsapp_link')
fmmods_fmwhatsapp_link = os.environ.get('fmmods_fmwhatsapp_link')
fmmods_gbwhatsapp_link = os.environ.get('fmmods_gbwhatsapp_link')
fmmods_yowhatsapp_link = os.environ.get('fmmods_yowhatsapp_link')

sammods_whatsapp_link = os.environ.get('sammods_whatsapp_link')
sammods_gbwhatsapp_link = os.environ.get('sammods_gbwhatsapp_link')
sammods_gbwhatsapp2_link = os.environ.get('sammods_gbwhatsapp2_link')
sammods_gbwhatsapp3_link = os.environ.get('sammods_gbwhatsapp3_link')

# Define the whatsapp_command function to handle the /whatsapp command
async def whatsapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton('Fouad Mods', callback_data='fouad')],
        [InlineKeyboardButton('Sam Mods', callback_data='sam')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select a WhatsApp mod:', reply_markup=reply_markup)



async def send_fouad_mod_options(query):
    await query.message.edit_text(text="Download Fouad Mod Whatsapp APK files - Fouad Mods")
    keyboard = [
        [InlineKeyboardButton('Whatsapp', callback_data='fmmods_whatsapp')],
        [InlineKeyboardButton('FM Whatsapp', callback_data='fmmods_fmwhatsapp')],
        [InlineKeyboardButton('GB Whatsapp', callback_data='fmmods_gbwhatsapp')],
        [InlineKeyboardButton('Yo Whatsapp', callback_data='fmmods_yowhatsapp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)


async def send_sam_mod_options(query):
    await query.message.edit_text(text="Download Mod WhatsApp APK Files - Sam Mods")
    keyboard = [
        [InlineKeyboardButton('com.whatsapp', callback_data='com_whatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp', callback_data='com_gbwhatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp2', callback_data='com_gbwhatsapp2')],
        [InlineKeyboardButton('com.gbwhatsapp3', callback_data='com_gbwhatsapp3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)


async def send_fmmods_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_whatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your Mod Whatsapp Apk file")



async def send_fmmods_fm_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_fmwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your FM Whatsapp Apk file")


async def send_fmmods_gb_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_gbwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your GB Whatsapp Apk file")


async def send_fmmods_yo_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_yowhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your YO Whatsapp Apk file")

async def send_com_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_whatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your Mod Whatsapp Apk file")



async def send_com_gbwhatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your FM Whatsapp Apk file")


async def send_com_gbwhatsapp2_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp2_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your GB Whatsapp Apk file")


async def send_com_gbwhatsapp3_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp3_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your YO Whatsapp Apk file")


async def send_fouad_mod_options_inline(update: Update):
    user_id = str(update.message.from_user.id)

    # Create an inline keyboard with the options
    keyboard = [
        [InlineKeyboardButton('Whatsapp', callback_data='fmmods_whatsapp')],
        [InlineKeyboardButton('FM Whatsapp', callback_data='fmmods_fmwhatsapp')],
        [InlineKeyboardButton('GB Whatsapp', callback_data='fmmods_gbwhatsapp')],
        [InlineKeyboardButton('Yo Whatsapp', callback_data='fmmods_yowhatsapp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message to the user
    await update.message.reply_text('Download Fouad Mod Whatsapp APK files:', reply_markup=reply_markup)

async def send_sam_mod_options_inline(update: Update):
    user_id = str(update.message.from_user.id)

    # Create an inline keyboard with the options
    keyboard = [
        [InlineKeyboardButton('com.whatsapp', callback_data='com_whatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp', callback_data='com_gbwhatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp2', callback_data='com_gbwhatsapp2')],
        [InlineKeyboardButton('com.gbwhatsapp3', callback_data='com_gbwhatsapp3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message to the user
    await update.message.reply_text('Download Sam Mod Whatsapp APK files:', reply_markup=reply_markup)






