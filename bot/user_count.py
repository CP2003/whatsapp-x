

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
