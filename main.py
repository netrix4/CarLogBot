from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackContext, CallbackQueryHandler

from Utils.TelegramApiData import TelegramApiData
import Controller.AddUserController as AddUserController
import Controller.AddQrController as AddQrController
import Controller.ImageReplyController as ImageReplyController


OBTENER_NOMBRENICK, OBTENER_OCUPATTION  = range(2)

api_data = TelegramApiData()
app = ApplicationBuilder().token(api_data.ApiToken).build()

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
app.add_handler(CommandHandler("dumb", reply_as_dumb))
app.add_handler(CommandHandler("kb", reply_register))
app.add_handler(MessageHandler(filters.PHOTO, reply_photo))

app.add_handler(AddUserController.whole_register_controller)
app.add_handler(AddQrController.add_new_qr_controller)
# app.add_handler(CallbackQueryHandler(AddQrController.qr_type_menu_handler, pattern="(QrFor[A-Za-z]+)"))

app.add_handler(CallbackQueryHandler(main_menu_handler, pattern="^Opcion[A-Z]+"))
# app.add_handler(CallbackQueryHandler(AddQrController.add_new_qr_controller, pattern="(QrFor[A-Za-z]+)"))

print("Bot iniciado")

app.run_polling(allowed_updates=Update.ALL_TYPES)