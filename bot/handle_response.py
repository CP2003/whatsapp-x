from telegram import InlineKeyboardButton , InlineKeyboardMarkup

def handle_response(text: str):
    processed = text.lower()

    if 'whatsapp' in processed:
    # Send reply message with inline buttons
        keyboard = [
        [InlineKeyboardButton('Fouad Mods', callback_data='fouad')],
        [InlineKeyboardButton('Sam Mods', callback_data='sam')]
         ]    
        reply_markup = InlineKeyboardMarkup(keyboard)
        return 'Please select your Whatsapp:', reply_markup

    return f"\"{text}\" is not in my data basse  \n \n \n  Try /help to get commands", None
