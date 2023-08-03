import os 
import asyncio
from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    await context.bot.send_chat_action(chat_id=user_id, action='typing')
    await asyncio.sleep(1)
    message = await update.message.reply_text('/whatsapp')
    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user_id, message_id=message.message_id, text='/whatsapp  -  to get WhatsApp mod apks')
