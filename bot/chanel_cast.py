import os
from telegram import Update
from telegram.ext import ContextTypes
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
async def chanel_cast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    # Broadcast the message to your channel
    chat_id = "-1001739683590"  # Replace with your channel username or chat_id
    message_text = replied_message.text
    reply_markup = replied_message.reply_markup

    try:
        # Send the broadcast message with the same inline keyboard
        await context.bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
        await update.message.reply_text(f"Message successfully sent fouad_whatsapp_updates channel")
    except telegram.error.BadRequest:
        await update.message.reply_text("Failed to send message to your channel. Please check your channel username or chat_id.")
