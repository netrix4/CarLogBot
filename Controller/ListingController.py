from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

from Utils.TelegramApiData import TelegramApiData
import Controller.AddUserController as AddUserController
import Controller.AddQrController as AddQrController
import Controller.ImageReplyController as ImageReplyController
import Controller.QrConversationcontroller as QrConversationController

async def reply_list_of_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_to_list = context._user_id
    list_of_car_qrs = AddQrController.get_cars(id_to_list)
    list_of_belongings_qrs = AddQrController.get_belongings(id_to_list)

    formated_results = "Estos son los resultados que encontré:\nCarros 🚗:\n"
    counter = 0
    for car in list_of_car_qrs:
        counter += 1
        formated_results += f'{counter:02d} - Marca:{car["Make"]} Modelo:{car["Model"]} Color:{car["Color"]}\n'
    counter = 0
    formated_results+="\nPertenencias 🎒:\n"
    for car in list_of_belongings_qrs:
        counter += 1
        formated_results += f'{counter:02d} - Descripción:{car["Description"]} ¿Perdido?:{car["IsLost"]}\n'

    await update.message.reply_text(formated_results)

async def reply_list_of_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_to_list = context._user_id
    list_of_messages = QrConversationController.get_messages(id_to_list)

    formated_results = "Estos son los mensajes que encontré 🎫:\n"

    counter = 0
    for message in list_of_messages:
        counter += 1
        formated_results += f'{counter:02d} - Titulo: {message["Title"]}\nContenido: {message["Content"]}\n'
    counter = 0
    

    await update.message.reply_text(formated_results)

listing_qrs_controller = CommandHandler("qrs", reply_list_of_qr)
listing_messages_controller = CommandHandler("messages", reply_list_of_messages)