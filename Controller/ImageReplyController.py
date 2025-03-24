import cv2
import requests

from telegram import Update, Bot
from telegram.ext import ContextTypes

from Utils.TelegramApiData import TelegramApiData
import Controller.qrRecognition as qrRecognition

api_data = TelegramApiData()

async def get_qr_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_id = update.effective_message.photo[-1].file_id
    # print(photo_id)

    temp = Bot(token=api_data.ApiToken)
    actual_file = await temp.get_file(photo_id)
    # print(actual_file)
    response = requests.get(actual_file.file_path)

    if response.status_code == 200:
        with open("temp.jpg", "wb") as file:
            file.write(response.content) 
        image = cv2.imread("temp.jpg")
        if image is not None:
            cv2.imwrite("./Images/processed_temp.jpg", image)  

    qrRecognition.read_QR("./Images/processed_temp.jpg")