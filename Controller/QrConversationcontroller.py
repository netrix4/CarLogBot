import random, math, json
from telegram import Update
from telegram.ext import filters, CommandHandler, ContextTypes, MessageHandler, ConversationHandler

import Controller.DataBaseConnector as DataBaseConnector
import Controller.ImageReplyController as ImageReplyController

OBTENER_QR, OBTENER_TITULO, OBTENER_MENSAJE = range(3)

async def start_qr_report_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reportar problema por QR 🚨. Dame el QR:")
    return OBTENER_QR

async def ask_for_title_and_save_qr_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_content = await ImageReplyController.get_qr_info(update, context)
    qr_data = json.loads(qr_content)
    context.user_data["qr_receiver_id"] = qr_data["OwnerId"]

    await update.message.reply_text("¿Qué problema quieres reportar? 🚨\nDame el asunto de tu mensaje para el/la responsable:")
    return OBTENER_TITULO

async def ask_for_content_and_save_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text

    await update.message.reply_text(f'Dame el contenido del mensaje que quieres alertarle el/la responsable: 🗒️')
    return OBTENER_MENSAJE

async def save_message_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text

    newMessage = {
        "Id": math.ceil(random.uniform(9,9999)),
        "Title": context.user_data["title"],
        "Content": context.user_data["message"],
        "ReceiverId": context.user_data["qr_receiver_id"]
    }

    DataBaseConnector.agregar_mensaje_local(newMessage)
    await update.message.reply_text(f'Mensaje agregado. Gracias ✅')
    return ConversationHandler.END

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text(f"Alerta cancelada ❎")
    return ConversationHandler.END

def get_messages(id_to_search):
    try:
      return DataBaseConnector.get_messages_by_user_id(id_to_search=id_to_search)
    except ValueError:
      return [{"error":"Something went wrong {ValueError}"}]

qr_report_controller =  ConversationHandler(
    entry_points=[CommandHandler("report", start_qr_report_conversation)],
    states={
        OBTENER_QR:[MessageHandler(filters.PHOTO & ~filters.COMMAND, ask_for_title_and_save_qr_info)],
        OBTENER_TITULO:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_content_and_save_title)],
        OBTENER_MENSAJE:[MessageHandler(filters.TEXT & ~filters.COMMAND, save_message_content)]
    },
    fallbacks=[CommandHandler("cancel", cancel_register)]
)