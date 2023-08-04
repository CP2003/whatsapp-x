import os
from telegram import Update
from telegram.ext import ContextTypes
import psycopg2
from .interacted_user import interacted_users, create_interacted_users_table, load_interacted_users_from_database, save_interacted_users

# Assuming you have already initialized interacted_users set and other variables

DATABASE_URL = os.environ.get('DATABASE_URL')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')

async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Calculate the user count (excluding the admin)
    user_count = len(interacted_users) - 1

    # Send the user count to the admin
    await update.message.reply_text(f"Total user count: {user_count}")



