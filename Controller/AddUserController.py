from telegram import Update
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler

from ConectaByPosgre.insercion import insert_user

OBTENER_NOMBRENICK, OBTENER_OCUPATTION  = range(2)

async def ask_for_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dame tu nombre o apodo 👤")
    return OBTENER_NOMBRENICK

async def ask_for_ocupattion_and_save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Obtener el ID de Telegram como identificador único
    context.user_data["user_id"] = user_id
    context.user_data["namenick"] = update.message.text
    await update.message.reply_text("Dame tu rol o actividad en la escuela 👤")
    return OBTENER_OCUPATTION

async def save_ocupattion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data["user_id"]
    context.user_data["ocupattion"] = update.message.text
    await update.message.reply_text(f'Datos agregados. Gracias, {context.user_data["namenick"]} ✅')

    new_user = {
        "FullName": context.user_data["namenick"],
        "Ocupattion": context.user_data["ocupattion"]
    }

    insert_user(int(user_id), new_user)  # Insertar en la base de datos PostgreSQL
    return ConversationHandler.END

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text(f"Registro cancelado ❎")
    return ConversationHandler.END

whole_register_controller = ConversationHandler(
    entry_points=[CommandHandler("register", ask_for_name)],
    states={
        OBTENER_NOMBRENICK: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_ocupattion_and_save_name)],
        OBTENER_OCUPATTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_ocupattion)],
    },
    fallbacks=[CommandHandler("cancelar", cancel_register)]
)