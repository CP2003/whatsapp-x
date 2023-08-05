import os
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ContextTypes , Updater

from .interacted_user import interacted_users, create_interacted_users_table, load_interacted_users_from_database, save_interacted_users
from .whatsapp import send_fouad_mod_options_inline, send_sam_mod_options_inline

BOT_USERNAME = os.environ.get('BOT_USERNAME')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
DATABASE_URL = os.environ.get('DATABASE_URL')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    command = context.args[0] if context.args else ''
    new_user_name = update.message.from_user.first_name

    # Check if the user is not already in interacted_users
    if user_id not in interacted_users:
        interacted_users.add(user_id)
        save_interacted_users()

        # Notify the admin about the new user
        if user_id != ADMIN_USER_ID:
            user_count = len(interacted_users) - 1
            admin_message = f"🆕 New User!\nTotal: {user_count}\nName: {new_user_name}"
            try:
                await context.bot.send_message(chat_id=ADMIN_USER_ID, text=admin_message)
            except telegram.error.BadRequest:
                print(f"Failed to send message to admin {ADMIN_USER_ID}")

    elif command == 'send_fouad':
        await context.bot.send_chat_action(chat_id=user_id, action='typing')
        await asyncio.sleep(1)
        await send_fouad_mod_options_inline(update)

    elif command == 'send_sam':
        await context.bot.send_chat_action(chat_id=user_id, action='typing')
        await asyncio.sleep(1)
        await send_sam_mod_options_inline(update)

    else:
        keyboard = [
            [InlineKeyboardButton('Telegram Chanel', url="https://t.me/fouad_whatsapp_updates")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('📥 Hi dear , Welcome', reply_markup=reply_markup)


