import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.handle_response import handle_response

ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
BOT_USERNAME = os.environ.get('BOT_USERNAME')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id: str = str(update.message.chat.id)
    username: str = update.message.from_user.username
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name

    if not username:
        username = f"{first_name} {last_name}" if first_name and last_name else "Anonymous"
    else:
        username = f"@{username}"

    if user_id == ADMIN_USER_ID:
        user_id = "Admin"
        username = "@Admin"

    print(f' {username} in {message_type}: "{text}"')

    # Sending the message to your group (replace -100123456789 with your group chat_id)
    group_chat_id = -707701170
    await context.bot.send_message(chat_id=group_chat_id, text=f'{username} in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response, reply_markup = handle_response(new_text)
            if 'reply_markup' in update.message:
                reply_markup = update.message.reply_markup
        else:
            return
    else:
        response, reply_markup = handle_response(text)

    if reply_markup is not None:
        await update.message.reply_text(response, reply_markup=reply_markup)
    else:
        await update.message.reply_text(response)

