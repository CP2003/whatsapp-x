import os , json , re
import psycopg2
from typing import Final
from telegram import Bot , Update, InlineKeyboardMarkup, InlineKeyboardButton ,InlineQueryResultArticle, InputTextMessageContent ,InlineQueryResultDocument 
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes , InlineQueryHandler , Updater
import telegram.error ,asyncio, time
import heroku3

from bot.start import start_command
from bot.help import help_command
from bot.interacted_user import interacted_users, create_interacted_users_table, load_interacted_users_from_database, save_interacted_users
from bot.user_count import count_command
from bot.whatsapp import whatsapp_command, send_fouad_mod_options, send_sam_mod_options, send_fmmods_whatsapp_file, send_fmmods_fm_whatsapp_file, send_fmmods_gb_whatsapp_file, send_fmmods_yo_whatsapp_file, send_com_whatsapp_file, send_com_gbwhatsapp_file, send_com_gbwhatsapp2_file, send_com_gbwhatsapp3_file, send_fouad_mod_options_inline, send_sam_mod_options_inline 
from bot.chanel_cast import chanel_cast_command
from bot.heroku import send_all_vars_command, edit_var_command 
from bot.inlinesearch import inline_search



print('Starting up bot...')
interacted_users = set()
TOKEN = os.environ.get('TOKEN')
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





def handle_response(text: str):
    processed = text.lower()

    return f"\"{text}\" is not in my data basse  \n \n \n  Try /help to get commands", None




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






async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    button = query.data

    if button == 'fmmods_whatsapp':
        await send_fmmods_whatsapp_file(query)
    elif button == 'fmmods_fmwhatsapp':
        await send_fmmods_fm_whatsapp_file(query)
    elif button == 'fmmods_gbwhatsapp':
        await send_fmmods_gb_whatsapp_file(query)
    elif button == 'fmmods_yowhatsapp':
        await send_fmmods_yo_whatsapp_file(query)
        
    if button == 'com_whatsapp':
        await send_com_whatsapp_file(query)
    elif button == 'com_gbwhatsapp':
        await send_com_gbwhatsapp_file(query)
    elif button == 'com_gbwhatsapp2':
        await send_com_gbwhatsapp2_file(query)
    elif button == 'com_gbwhatsapp3':
        await send_com_gbwhatsapp3_file(query)
    
    elif button == 'fouad':
        await send_fouad_mod_options(query)
    elif button == 'sam':
        await send_sam_mod_options(query)






def error(update, context):
    print(f'Update {update} caused an error: {context.error}')
    # You can handle errors here if needed


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('whatsapp', whatsapp_command))
    app.add_handler(CommandHandler('cast', cast_command))
    app.add_handler(CommandHandler('count', count_command))
    app.add_handler(CommandHandler('edit', edit_var_command))
    app.add_handler(CommandHandler('ccast', chanel_cast_command))
    app.add_handler(CommandHandler('allvar', send_all_vars_command))
    app.add_handler(InlineQueryHandler(inline_search))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.Text(), handle_message))
    app.add_error_handler(error)

    # Start the Bot



    print('Polling...')

    try:
        app.run_polling(poll_interval=3)
    finally:
        save_interacted_users()
        
  
