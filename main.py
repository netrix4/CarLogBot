from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler

from Utils.TelegramApiData import TelegramApiData
import Controller.ImageReplyController as ImageReplyController

api_data = TelegramApiData()
app = ApplicationBuilder().token(api_data.ApiToken).build()

async def reply_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a list action for listing all the provided data")
async def reply_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CarLog is intended as a class project for Backend-1")
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
app.add_handler(CommandHandler("about", reply_about))
app.add_handler(CommandHandler("list", reply_list))
app.add_handler(CommandHandler("dumb", reply_as_dumb))

print("Bot iniciado")
app.add_handler(MessageHandler(filters.PHOTO, reply_photo))

app.run_polling(allowed_updates=Update.ALL_TYPES)