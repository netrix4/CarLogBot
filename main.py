from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

from Utils.TelegramApiData import TelegramApiData
import Controller.AddUserController as AddUserController
import Controller.AddQrController as AddQrController
import Controller.ImageReplyController as ImageReplyController
import Controller.QrConversationcontroller as QrConversationController
import Controller.ListingController as ListingController

api_data = TelegramApiData()
app = ApplicationBuilder().token(api_data.ApiToken).build()

async def reply_invalid_text(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Invalid command, try the button bellow ⤵️ or these options:\n/whatup\n/dumb\n/kb\n/register\n/new")

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
app.add_handler(CommandHandler("dumb", reply_as_dumb))
# app.add_handler(MessageHandler(filters.PHOTO, reply_photo))

app.add_handler(ListingController.listing_qrs_controller)
app.add_handler(ListingController.listing_messages_controller)
app.add_handler(AddUserController.whole_register_controller)
app.add_handler(AddQrController.add_new_qr_controller)
app.add_handler(QrConversationController.qr_report_controller)

print("Bot iniciado")

app.run_polling(allowed_updates=Update.ALL_TYPES)
