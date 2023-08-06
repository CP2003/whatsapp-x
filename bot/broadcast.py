import os
from telegram import Update
from telegram.ext import ContextTypes

from bot.interacted_user import interacted_users, create_interacted_users_table, load_interacted_users_from_database, save_interacted_users

BOT_USERNAME = os.environ.get('BOT_USERNAME')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
DATABASE_URL = os.environ.get('DATABASE_URL')

async def cast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Get the replied message and use it as the broadcast message
    replied_message = update.message.reply_to_message
    if not replied_message:
        await update.message.reply_text("Please reply to a message to use it as the broadcast message.")
        return

    # Extract the message text and the inline keyboard from the replied message
    message_text = replied_message.text
    reply_markup = replied_message.reply_markup

    # Broadcast the message to all users (excluding the admin)
    successful_broadcasts = 0
    for user_id in interacted_users:
        if user_id != ADMIN_USER_ID:
            try:
                # Send the broadcast message with the same inline keyboard
                await context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup)
                successful_broadcasts += 1
            except telegram.error.BadRequest:
                print(f"Failed to send message to user {user_id}")

    # Format the success message with the user count
    user_count = successful_broadcasts
    await update.message.reply_text(f"Broadcast sent successfully to {user_count} users.")
