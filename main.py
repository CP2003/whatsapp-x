import os , json , re
import psycopg2
from typing import Final
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,InlineQueryResultArticle, InputTextMessageContent ,InlineQueryResultDocument 
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes , InlineQueryHandler
import telegram.error ,asyncio, time
import heroku3





print('Starting up bot....')
interacted_users = set()
TOKEN = os.environ.get('TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')

fmmods_whatsapp_link = os.environ.get('fmmods_whatsapp_link')
fmmods_fmwhatsapp_link = os.environ.get('fmmods_fmwhatsapp_link')
fmmods_gbwhatsapp_link = os.environ.get('fmmods_gbwhatsapp_link')
fmmods_yowhatsapp_link = os.environ.get('fmmods_yowhatsapp_link')

sammods_whatsapp_link = os.environ.get('sammods_whatsapp_link')
sammods_gbwhatsapp_link = os.environ.get('sammods_gbwhatsapp_link')
sammods_gbwhatsapp2_link = os.environ.get('sammods_gbwhatsapp2_link')
sammods_gbwhatsapp3_link = os.environ.get('sammods_gbwhatsapp3_link')

DATABASE_URL = os.environ.get('DATABASE_URL')
HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY')
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
if os.path.exists('interacted_users.json'):
    try:
        with open('interacted_users.json', 'r') as file:
            interacted_users = set(json.load(file))
    except (IOError, json.JSONDecodeError):
        print("Table interacted_users creating...")
        interacted_users = set()
else:
    # Create the file if it does not exist
    with open('interacted_users.json', 'w') as file:
        json.dump(list(interacted_users), file)




async def admin_cast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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









def mono_effect(key, value):
    return f"`⭕️ {key} : {value}`"

async def send_all_vars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_USER_ID:
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






# ... Your existing code ...

def get_bot_users_first_names():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name FROM interacted_users")
                rows = cur.fetchall()
                return [first_name[0] for first_name in rows]
    except psycopg2.Error as e:
        print(f'Error fetching bot users: {e}')
        return []

async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name FROM users")
                rows = cur.fetchall()

        if not rows:
            await update.message.reply_text("No users found.")
        else:
            user_names = [row[0] for row in rows]
            user_list = "\n".join(user_names)
            await update.message.reply_text(f"List of Bot Users:\n\n{user_list}")
    except psycopg2.Error as e:
        await update.message.reply_text("Failed to fetch bot users. Please try again later.")
        print(f'Error fetching bot users: {e}')























def create_interacted_users_table():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS interacted_users (
                        user_id TEXT PRIMARY KEY
                    )
                    """
                )
        print('Table interacted_users created successfully.')
    except psycopg2.Error as e:
        print(f'Failed to create table interacted_users: {e}')

def load_interacted_users_from_database():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM interacted_users")
                rows = cur.fetchall()
                return set(user_id[0] for user_id in rows)
    except psycopg2.Error as e:
        print(f'Error loading interacted_users from the database. Starting with an empty set. {e}')
        return set()

create_interacted_users_table()
interacted_users = load_interacted_users_from_database()

# ... Other code ...

def save_interacted_users():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM interacted_users")  # Clear the table before saving new data

                for user_id in interacted_users:
                    try:
                        cur.execute("INSERT INTO interacted_users (user_id) VALUES (%s)", (user_id,))
                    except psycopg2.Error as e:
                        conn.rollback()  # Roll back the transaction in case of error
                        print(f"Failed to insert user_id {user_id}: {e}")

                conn.commit()  # Commit the transaction after all data is inserted

        print('Data successfully saved to the database.')

    except psycopg2.Error as e:
        print(f'Failed to save interacted_users data to the database: {e}')






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




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    await context.bot.send_chat_action(chat_id=user_id, action='typing')
    await asyncio.sleep(1)
    message = await update.message.reply_text('/whatsapp')
    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user_id, message_id=message.message_id, text='/whatsapp  -  to get whatsapp mod apks')

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

def handle_response(text: str):
    processed = text.lower()

    if 'whatsapp' in processed:
        # Send reply message with inline buttons for selecting the mod
        keyboard = [
            [InlineKeyboardButton('Fouad Mods', callback_data='fouad')],
            [InlineKeyboardButton('Sam Mods', callback_data='sam')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        return 'Select a WhatsApp mod:', reply_markup

    return f"\"{text}\" is not in my data basse  \n \n \n  Try /help to get commands", None


async def send_fouad_mod_options(query):
    await query.message.edit_text(text="Download Fouad Mod Whatsapp APK files - Fouad Mods")
    keyboard = [
        [InlineKeyboardButton('Whatsapp', callback_data='fmmods_whatsapp')],
        [InlineKeyboardButton('FM Whatsapp', callback_data='fmmods_fmwhatsapp')],
        [InlineKeyboardButton('GB Whatsapp', callback_data='fmmods_gbwhatsapp')],
        [InlineKeyboardButton('Yo Whatsapp', callback_data='fmmods_yowhatsapp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)


async def send_sam_mod_options(query):
    await query.message.edit_text(text="Download Mod WhatsApp APK Files - Sam Mods")
    keyboard = [
        [InlineKeyboardButton('com.whatsapp', callback_data='com_whatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp', callback_data='com_gbwhatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp2', callback_data='com_gbwhatsapp2')],
        [InlineKeyboardButton('com.gbwhatsapp3', callback_data='com_gbwhatsapp3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)





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


async def send_fmmods_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_whatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your Mod Whatsapp Apk file")



async def send_fmmods_fm_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_fmwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your FM Whatsapp Apk file")


async def send_fmmods_gb_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_gbwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your GB Whatsapp Apk file")


async def send_fmmods_yo_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=fmmods_yowhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your YO Whatsapp Apk file")

async def send_com_whatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_whatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your Mod Whatsapp Apk file")



async def send_com_gbwhatsapp_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your FM Whatsapp Apk file")


async def send_com_gbwhatsapp2_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp2_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your GB Whatsapp Apk file")


async def send_com_gbwhatsapp3_file(query):
    await query.message.edit_text(text="Uploading Your File")
    await query.message.chat.send_action(action='upload_document')
    await asyncio.sleep(3)
    await query.message.reply_document(document=sammods_gbwhatsapp3_link)
    await asyncio.sleep(1)
    await query.message.edit_text(text="Here is Your YO Whatsapp Apk file")


async def send_fouad_mod_options_inline(update: Update):
    user_id = str(update.message.from_user.id)

    # Create an inline keyboard with the options
    keyboard = [
        [InlineKeyboardButton('Whatsapp', callback_data='fmmods_whatsapp')],
        [InlineKeyboardButton('FM Whatsapp', callback_data='fmmods_fmwhatsapp')],
        [InlineKeyboardButton('GB Whatsapp', callback_data='fmmods_gbwhatsapp')],
        [InlineKeyboardButton('Yo Whatsapp', callback_data='fmmods_yowhatsapp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message to the user
    await update.message.reply_text('Download Fouad Mod Whatsapp APK files:', reply_markup=reply_markup)

async def send_sam_mod_options_inline(update: Update):
    user_id = str(update.message.from_user.id)

    # Create an inline keyboard with the options
    keyboard = [
        [InlineKeyboardButton('com.whatsapp', callback_data='com_whatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp', callback_data='com_gbwhatsapp')],
        [InlineKeyboardButton('com.gbwhatsapp2', callback_data='com_gbwhatsapp2')],
        [InlineKeyboardButton('com.gbwhatsapp3', callback_data='com_gbwhatsapp3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message to the user
    await update.message.reply_text('Download Sam Mod Whatsapp APK files:', reply_markup=reply_markup)



async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []

    try:
        if 'whats' in query:
            # First result: Fouad Mod Whatsapp
            fouad_button = InlineKeyboardButton('Fouad Mod Whatsapp', url=f'https://t.me/{BOT_USERNAME}?start=send_fouad')
            # Second result: Sam Mods Whatsapp
            sam_button = InlineKeyboardButton('Sam Mods Whatsapp', url=f'https://t.me/{BOT_USERNAME}?start=send_sam')

            reply_markup = InlineKeyboardMarkup([[fouad_button], [sam_button]])

            # Add the results to the list
            results.append(
                InlineQueryResultArticle(
                    id='1',
                    title='Fouad Mod Whatsapp',
                    input_message_content=InputTextMessageContent(
                        message_text='Please select a WhatsApp mod:'
                    ),
                    description='Download Fouad Mod Whatsapp APK files',
                    reply_markup=reply_markup
                )
            )

    except telegram.error.BadRequest:
        pass  # Ignore the "Query is too old" error

    await update.inline_query.answer(results, cache_time=0)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused an error: {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cast', cast_command))
    app.add_handler(CommandHandler('count', count_command))
    app.add_handler(CommandHandler('edit', edit_var_command))
    app.add_handler(CommandHandler('ccast', admin_cast_command))
    app.add_handler(CommandHandler('allvar', send_all_vars_command))
    app.add_handler(CommandHandler('users', send_users_command))
    app.add_handler(InlineQueryHandler(inline_search))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.Text(), handle_message))
    app.add_error_handler(error)

    print('Polling...')

    try:
        app.run_polling(poll_interval=3)
    finally:

        save_interacted_users()
        conn.close()
