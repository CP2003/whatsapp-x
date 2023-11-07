import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import heroku3
from Database.data import *


HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY')
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')


# Define a function to restart your Heroku app
def restart_bot(update, context):
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        app = heroku_conn.app('YOUR_APP_NAME')  # Replace 'YOUR_APP_NAME' with your Heroku app name
        dyno = app.dynos()[0]
        dyno.restart()
        update.message.reply_text("Bot is restarting...")
    except Exception as e:
        update.message.reply_text(f"Failed to restart the bot: {e}")

async def send_all_vars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Get all Heroku environment variables
    try:
        heroku_conn = heroku3.from_key(HEROKU_API_KEY)
        app = heroku_conn.apps()[HEROKU_APP_NAME]
        config_vars = app.config().to_dict()

    except Exception as e:
        await update.message.reply_text("Failed to fetch Heroku environment variables. Please check your Heroku API key and app name.")
        print(f'Error fetching Heroku environment variables: {e}')
    else:
        # Format the environment variables as a string with a new line between each variable
        all_vars = "\n\n".join([mono_effect(key, value) for key, value in config_vars.items()])

        # Send the environment variables to the admin in a private chat
        await context.bot.send_message(chat_id=ADMIN_USER_ID, text=all_vars, disable_web_page_preview=True, parse_mode='Markdown')
        await update.message.reply_text("All Heroku environment variables sent to the admin in a private chat.")




def edit_heroku_vars(var_name, var_value):
    if HEROKU_API_KEY and HEROKU_APP_NAME:
        heroku_conn = heroku3.from_key(HEROKU_API_KEY)
        app = heroku_conn.apps()[HEROKU_APP_NAME]
        
        try:
            app.config()[var_name] = var_value
            print(f'Successfully updated Heroku environment variable: {var_name}')
            return True
        except Exception as e:
            print(f'Failed to update Heroku environment variable: {e}')
            return False
    else:
        return False

async def edit_var_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Parse the command arguments (variable name and value)
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Please provide the variable name and its new value in the format `/edit VAR_NAME VAR_VALUE`.")
        return

    var_name, var_value = args

    # Edit the Heroku environment variable
    result = edit_heroku_vars(var_name, var_value)

    if result:
        await update.message.reply_text(f"Successfully updated Heroku environment variable: {var_name}")
    else:
        await update.message.reply_text("Failed to update the Heroku environment variable. Please check your Heroku API key and app name.")

