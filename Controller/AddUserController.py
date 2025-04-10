from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, CallbackQueryHandler

import Controller.DataBaseConnector as DataBaseConnector
# Estados del flujo conversacional
OBTENER_NOMBRENICK, OBTENER_OCUPATTION  = range(2)

# Paso 1: Solicita el nombre o apodo del usuario
async def ask_for_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dame tu nombre o apodo 👤")
    return OBTENER_NOMBRENICK
# Paso 2: Guarda el nombre/apodo y solicita la ocupación mediante botones
async def ask_for_ocupattion_and_save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = update.message.from_user.id  
    user_id = context._user_id #Obtener el ID de Telegram como identificador único
    context.user_data["user_id"] = user_id# Obtenemos el ID encriptado del usuario
    context.user_data["namenick"] = update.message.text # Guardamos el nombre o apodo

    # Creamos teclado con botones para elegir ocupación
    register_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Estudiante", callback_data="ocupattion:Estudiante")
        ],
        [
            InlineKeyboardButton(text="Docente/Administrativo", callback_data="ocupattion:Docente/Adimnistrativo")
        ]
        ])
    
    await update.message.reply_text("Dame tu rol o actividad en la escuela 👤💾 ", reply_markup=register_keyboard)

    return OBTENER_OCUPATTION
# Paso 3: Guarda la ocupación seleccionada y registra al usuario en la base de datos
async def save_ocupattion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtenemos el valor real de la ocupación desde el botón
    await update.callback_query.answer()
    ocupation = update.callback_query.data.replace('ocupattion:', '')
    context.user_data["ocupattion"] = ocupation

    await update.callback_query.message.reply_text(f'Datos agregados. Gracias, {context.user_data["namenick"]} ✅')
    # Construimos el objeto del nuevo usuario
    newUser = {
        "Id": context.user_data["user_id"],
        "FullName": context.user_data["namenick"],
        "Ocupattion": context.user_data["ocupattion"]
    }
    # Guardamos al usuario en la base de datos (PostgreSQL)
    DataBaseConnector.insert_user_postgres(int(newUser["Id"]), newUser)  # Insertar en la base de datos PostgreSQL
    #DataBaseConnector.insert_user_local(newUser)
    
    return ConversationHandler.END
# Comando para cancelar el proceso de registro
async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text(f"Registro cancelado ❎")
    return ConversationHandler.END

whole_register_controller = ConversationHandler(
    entry_points=[CommandHandler("register", ask_for_name)],
    states={
        OBTENER_NOMBRENICK:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_ocupattion_and_save_name)],
        OBTENER_OCUPATTION:[CallbackQueryHandler(save_ocupattion, pattern='((ocupattion:)[A-Za-z/]+)')],
    },
    fallbacks=[CommandHandler("cancel", cancel_register)]
)