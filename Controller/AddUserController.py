from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, CallbackQueryHandler

from ConectaByPosgre.insercion import insert_user
import Controller.DataBaseConnector as DataBaseConnector

OBTENER_NOMBRENICK, OBTENER_OCUPATTION  = range(2)

async def ask_for_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dame tu nombre o apodo 👤")
    return OBTENER_NOMBRENICK

async def ask_for_ocupattion_and_save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = update.message.from_user.id  # Obtener el ID de Telegram como identificador único
    user_id = context._user_id
    context.user_data["user_id"] = user_id
    context.user_data["namenick"] = update.message.text

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

async def save_ocupattion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()
    ocupation = update.callback_query.data.replace('ocupattion:', '')
    context.user_data["ocupattion"] = ocupation

    await update.callback_query.message.reply_text(f'Datos agregados. Gracias, {context.user_data["namenick"]} ✅')

    newUser = {
        "Id": context.user_data["user_id"],
        "FullName": context.user_data["namenick"],
        "Ocupattion": context.user_data["ocupattion"]
    }

    # insert_user(int(newUser["Id"]), newUser)  # Insertar en la base de datos PostgreSQL
    DataBaseConnector.agregar_usuario_local(newUser)
    
    return ConversationHandler.END

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