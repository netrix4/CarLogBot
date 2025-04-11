from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, CallbackContext, CallbackQueryHandler

import Controller.DataBaseConnector as DataBaseConnector
import Controller.ImagesHandler as ImagesHandler
import math,random, json

#states of conversation
OBTENER_TIPOQR, OBTENER_DETALLES  = range(2)
# Step 1: Ask the user what type of QR he/she wants to generate.
async def ask_for_qr_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Para Carro 🚗🏷️", callback_data="QrForCar"),
            InlineKeyboardButton(text="Para Pertenencia 🎒🏷️", callback_data="QrForBelonging")
        ]
    ])
    await update.message.reply_text("¿Qué tipo de QR quieres generar? 🏷️", reply_markup=qr_keyboard)
    return OBTENER_TIPOQR

# Step 2: Manage the QR type selected from the menu
async def qr_type_menu_handler(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    button_data = update.callback_query.data
    context.user_data["qr_type"] = button_data # Guardamos el tipo de QR en los datos del usuario

    # Enviar instrucciones específicas según el tipo de QR
    if button_data == "QrForCar":
        await update.callback_query.message.reply_text("Seleccionaste Carro, separado por espacios, dame:\nMarca\nModelo\nColor")
    elif button_data == "QrForBelonging":
        await update.callback_query.message.reply_text("Seleccionaste Pertenencia, separado por espacios, dame:\nUna descripción de la pertenencia")
    return OBTENER_DETALLES
# Paso 3: Guardar los detalles proporcionados y generar QR
async def save_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # ID del usuario en Telegram
    detalles = update.message.text.split()# Dividir el mensaje en palabras
    tipo_qr = context.user_data["qr_type"] # Obtener el tipo de QR guardado anteriormente

    if tipo_qr:
         # Crear entrada si es QR para carro y se dieron al menos 3 datos
        if tipo_qr == "QrForCar" and len(detalles) >= 3:
            car_id = random.randint(2000, 9999)  # # ID único para la base de datos
            newEntry = {
                "Id": math.ceil(random.uniform(9,9999)), # ID interno único
                "Make": detalles[0],
                "Model": detalles[1],
                "Color": detalles[2],
                "OwnerId": context._user_id # ID encriptado del usuario
            }
            # Guardar en base de datos Postgres
            DataBaseConnector.insert_car_postgres(car_id, user_id, newEntry)
            #DataBaseConnector.insert_car_local(newEntry)
        # Crear entrada si es QR para pertenencia
        elif tipo_qr == "QrForBelonging":
            belonging_id = random.randint(3000, 9999) 
            newEntry = {
                "Id": math.floor(random.uniform(9,9999)),# ID interno único
                "Description": update.message.text,# Todo el texto como descripción
                "IsLost": False,
                "OwnerId": context._user_id
            }
            # Guardar en base de datos Postgres
            DataBaseConnector.insert_belonging_postgres(belonging_id, user_id, newEntry)
            #DataBaseConnector.insert_belonging_local(newEntry)
    
        try:
              # Generar el código QR con los datos del objeto
             qr_file_path = ImagesHandler.generate_QR(json.dumps(newEntry), newEntry["OwnerId"])
             # Enviar imagen del QR al usuario
             await update.message.reply_photo(photo=open(qr_file_path, 'rb'), caption="Aquí está tu nuevo QR, Guárdalo bien.")
             #await update.message.reply_photo(photo=open(f'./Images/SuperSecretData-{newEntry["OwnerId"]}.jpg', 'rb'), caption="Aquí está tu nuevo QR, Guardalo bien.")
        except Exception as e:      
          print('An exception occurred')
          print("🔴 ERROR GENERANDO QR O ENVIANDO IMAGEN:", e)

    else:
        # En caso de error de formato
        await update.message.reply_text("Formato incorrecto, intenta de nuevo ❌")
        return OBTENER_DETALLES
    return ConversationHandler.END
# Manejo de cancelación de la creación de QR
async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text("Registro de QR cancelado ❎")
    return ConversationHandler.END
# Controlador principal del flujo de creación de QR
add_new_qr_controller = ConversationHandler(
    entry_points=[CommandHandler("new", ask_for_qr_type)],
    states={
        OBTENER_TIPOQR: [CallbackQueryHandler(qr_type_menu_handler, pattern="QrFor[A-Za-z]+")],
        OBTENER_DETALLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_details)],
    },
    fallbacks=[CommandHandler("cancelar", cancel_register)]
)
