from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, InlineQueryHandler

from bot.whatsapp import whatsapp_command, send_fouad_mod_options, send_sam_mod_options, send_fmmods_whatsapp_file, send_fmmods_fm_whatsapp_file, send_fmmods_gb_whatsapp_file, send_fmmods_yo_whatsapp_file, send_com_whatsapp_file, send_com_gbwhatsapp_file, send_com_gbwhatsapp2_file, send_com_gbwhatsapp3_file, send_fouad_mod_options_inline, send_sam_mod_options_inline 
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


