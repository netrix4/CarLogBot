from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, CallbackContext, CallbackQueryHandler

import Controller.DataBaseConnector as DataBaseConnector
import Controller.ImagesHandler as ImagesHandler
import math,random, json

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
        await update.callback_query.message.reply_text("Seleccionaste Carro, separado por espacios, dame:\nMarca\nModelo\nColor")
    elif button_data == "QrForBelonging":
        await update.callback_query.message.reply_text("Seleccionaste Pertenencia, separado por espacios, dame:\nUna descripción de la pertenencia")
    return OBTENER_DETALLES

async def save_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # ID del usuario en Telegram
    detalles = update.message.text.split()
    tipo_qr = context.user_data["qr_type"]

    if tipo_qr:

        if tipo_qr == "QrForCar" and len(detalles) >= 3:
            car_id = random.randint(2000, 9999)  # Generar ID único
            newEntry = {
                "Id": math.ceil(random.uniform(9,9999)),
                "Make": detalles[0],
                "Model": detalles[1],
                "Color": detalles[2],
                "OwnerId": context._user_id
            }
            # DataBaseConnector.insert_car_postgres(car_id, user_id, newEntry)
            DataBaseConnector.insert_car_local(newEntry)

        elif tipo_qr == "QrForBelonging":
            belonging_id = random.randint(3000, 9999)
            newEntry = {
                "Id": math.floor(random.uniform(9,9999)),
                "Description": update.message.text,
                "IsLost": False,
                "OwnerId": context._user_id
            }
            # DataBaseConnector.insert_belonging_postgres(belonging_id, user_id, newEntry)
            DataBaseConnector.insert_belonging_local(newEntry)
    
        try:
            ImagesHandler.generate_QR(json.dumps(newEntry), newEntry["OwnerId"])
            await update.message.reply_text('QR nuevo asociado. Gracias, ✅')
            await update.message.reply_photo(photo=open(f'./Images/SuperSecretData-{newEntry["OwnerId"]}.jpg', 'rb'), caption="Aquí está tu nuevo QR, Guardalo bien.")
        except:
          print('An exception occurred')

    else:
        await update.message.reply_text("Formato incorrecto, intenta de nuevo ❌")
        return OBTENER_DETALLES

    return ConversationHandler.END

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text("Registro de QR cancelado ❎")
    return ConversationHandler.END

add_new_qr_controller = ConversationHandler(
    entry_points=[CommandHandler("new", ask_for_qr_type)],
    states={
        OBTENER_TIPOQR: [CallbackQueryHandler(qr_type_menu_handler, pattern="QrFor[A-Za-z]+")],
        OBTENER_DETALLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_details)],
    },
    fallbacks=[CommandHandler("cancelar", cancel_register)]
)
