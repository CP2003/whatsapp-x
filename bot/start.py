import os 
import psycopg2
import json
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,InlineQueryResultArticle, InputTextMessageContent ,InlineQueryResultDocument 
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes , InlineQueryHandler

BOT_USERNAME = os.environ.get('BOT_USERNAME')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
DATABASE_URL = os.environ.get('DATABASE_URL')

interacted_users = set()


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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    print(ADMIN_USER_ID)
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

