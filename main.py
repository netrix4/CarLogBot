from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackContext, CallbackQueryHandler

import Controller.AddUserController as AddUserController

from Utils.TelegramApiData import TelegramApiData
import Controller.ImageReplyController as ImageReplyController


OBTENER_NOMBRENICK, OBTENER_OCUPATTION  = range(2)

api_data = TelegramApiData()
app = ApplicationBuilder().token(api_data.ApiToken).build()

async def reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Este es el boton a00", callback_data="OpcionA"),
            InlineKeyboardButton(text="Este es el boton a01", callback_data="OpcionB")
        ],
        [
            InlineKeyboardButton(text="Este es el boton a10", callback_data="OpcionC"),
            InlineKeyboardButton(text="Este es el boton a11", callback_data="OpcionD")
        ]
        ])
    
    # await update.message.reply_photo("Este es el menu de botones para...", reply_markup=keyboard)
    await update.message.reply_text("Este es el menu de botones para...", reply_markup=keyboard)

async def main_menu_handler(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    
    button_data = update.callback_query.data
    if button_data == "OpcionA":
        print("Presionaste el boton! A")
    if button_data == "OpcionB":
        print("Presionaste el boton! B")
    if button_data == "OpcionC":
        print("Presionaste el boton! C")
        
    await update.callback_query.message.reply_text(f"So this is {button_data}")

async def reply_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Agregar tu nombre o apodo", callback_data="add_name")
        ],
        [
            InlineKeyboardButton(text="Agregar rol en la escuela", callback_data="add_ocupattion")
        ]
        ])
    
    # await update.message.reply_photo("Este es el menu de botones para...", reply_markup=keyboard)
    await update.message.reply_text("Dame tu informacion para registrarte 💾 ", reply_markup=register_keyboard)

async def reply_whatup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("So whatup")
    
async def reply_as_dumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_params = ""
    for param in context.args:
        text_params += str(param) + " "
    await update.message.reply_text(f"Oh, did u mean {text_params}")

async def reply_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_id = ImageReplyController.get_qr_info(update, context)
    
    await update.message.reply_photo(photo_id, caption="Acaso esta es tu carta? 🎩")

app.add_handler(CommandHandler("whatup", reply_whatup))
app.add_handler(CommandHandler("menutest", reply_register))

app.add_handler(CallbackQueryHandler(main_menu_handler))
app.add_handler(CommandHandler("kb", reply_keyboard))

app.add_handler(CommandHandler("dumb", reply_as_dumb))
app.add_handler(MessageHandler(filters.PHOTO, reply_photo))

app.add_handler(AddUserController.whole_register_controller)

print("Bot iniciado")

app.run_polling(allowed_updates=Update.ALL_TYPES)