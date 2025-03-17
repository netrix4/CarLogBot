
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = ""
app = ApplicationBuilder().token(TOKEN).build()

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


app.add_handler(CommandHandler("whatup", reply_whatup))
app.add_handler(CommandHandler("about", reply_about))
app.add_handler(CommandHandler("list", reply_list))
app.add_handler(CommandHandler("dumb", reply_as_dumb))

app.run_polling(allowed_updates=Update.ALL_TYPES)