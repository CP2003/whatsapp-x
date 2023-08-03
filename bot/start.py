import os 
from telegram.ext import ContextTypes, CommandHandler
from telegram import Update


BOT_USERNAME = os.environ.get('BOT_USERNAME')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')

interacted_users = set()
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
            [InlineKeyboardButton('Telegram Chanel', url="https://t.me/fouad_whatsapp_updates")],
            [InlineKeyboardButton('Whatsapp Group', url="https://chat.whatsapp.com/HyBbE8HNwg6CblSfwuyqYR")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('📥 Hi dear , Welcome', reply_markup=reply_markup)
