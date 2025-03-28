from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, CallbackContext, CallbackQueryHandler

import Controller.DataBaseConnector as DataBaseConnector
import Controller.qrRecognition as QrRecognition
import random, math, json

OBTENER_TIPOQR, OBTENER_DETALLES  = range(2)

async def ask_for_qr_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Para Carro 🚗🏷️", callback_data="QrForCar"),
            InlineKeyboardButton(text="Para Pertenencia 🎒🏷️", callback_data="QrForBelonging")
        ]
    ])
    await update.message.reply_text("¿Qué tipo de QR quieres generar? 🏷️", reply_markup=qr_keyboard)
    return OBTENER_TIPOQR

async def qr_type_menu_handler(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    button_data = update.callback_query.data
    context.user_data["qr_type"] = button_data

    if button_data == "QrForCar":
        print("Presionaste el botón! Car")
        await update.callback_query.message.reply_text(
            "Seleccionaste Carro, separado por espacios, dame:\nMarca\nModelo\nColor"
        )
    if button_data == "QrForBelonging":
        print("Presionaste el botón! Belonging")
        await update.callback_query.message.reply_text(
            "Seleccionaste Pertenencia, separado por espacios, dame:\nUna descripción de la pertenencia"
        )

    return OBTENER_DETALLES

async def save_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    detalles = update.message.text.split()
    context.user_data["qr_details"] = detalles
    tipo_qr = context.user_data["qr_type"]

    if tipo_qr == "QrForCar":
        newEntry = {
            "Id": math.ceil(random.uniform(9,9999)),
            "Make": detalles[0],
            "Model": detalles[1],
            "Color": detalles[2],
            "OwnerId": context._user_id
        }
        # print(newCarQr)
    if tipo_qr == "QrForBelonging":
        newEntry = {
            "Id": math.floor(random.uniform(9,9999)),
            "Description": update.message.text,
            "IsLost": False,
            "OwnerId": context._user_id
        }
        # print(newBelongingQr)

    print(newEntry)     

    try:
        QrRecognition.generate_QR(json.dumps(newEntry), newEntry["OwnerId"])

        if tipo_qr == "QrForCar":
            DataBaseConnector.agregar_car_local(nuevo_objeto=newEntry)
        else:
            DataBaseConnector.agregar_belonging_local(nuevo_objeto=newEntry)

        await update.message.reply_text('QR nuevo asociado. Gracias, ✅')
        await update.message.reply_photo(photo=open(f'./Images/SuperSecretData-{newEntry["OwnerId"]}.jpg', 'rb'), caption="Aquí está tu nuevo QR, Guardalo bien.")

    except:
        await update.message.reply_text(f'Algo salio mal agregando tus datos ❌')

    return ConversationHandler.END

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text(f"Registro de QR cancelado ❎")
    return ConversationHandler.END

def get_cars(id_to_search):
    try:
      return DataBaseConnector.get_cars_by_user_id(id_to_search=id_to_search)
    except ValueError:
      return [{"error":"Something went wrong {ValueError}"}]
def get_belongings(id_to_search):
    try:
      return DataBaseConnector.get_belongings_by_user_id(id_to_search=id_to_search)
    except ValueError:
      return [{"error":"Something went wrong {ValueError}"}]

add_new_qr_controller = ConversationHandler(
    entry_points=[CommandHandler("new", ask_for_qr_type)],
    states={
        OBTENER_TIPOQR: [CallbackQueryHandler(qr_type_menu_handler, pattern="QrFor[A-Za-z]+")],
        OBTENER_DETALLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_details)],
    },
    fallbacks=[CommandHandler("cancelar", cancel_register)]
)