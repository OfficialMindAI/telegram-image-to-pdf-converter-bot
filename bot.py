from telegram import (
    Update, 
    BotCommand, 
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext, 
    MessageHandler, 
    AIORateLimiter,
    filters, 
) 
import os
import traceback
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

from pathlib import Path
from io import BytesIO 
from uuid import uuid4 

 



HELP_MESSAGE = """Commands:
⚪ /start – To start the bot 

🎨 Send an image and the bot will send you the image without background 
🎤 For issues, informations or advertising contact @MindAIOfficial
"""



input_path =  Path(__file__).parent.resolve() / "input_images"
output_path =  Path(__file__).parent.resolve() / "input_images"

def create_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")
 
async def handle_bg_remove(update: Update, context: CallbackContext):   
    new_file =  await update.message.photo[-1].get_file() 
    await new_file.download_to_drive(input_path / f"{new_file.file_id}.png") 
    image = Image.open(input_path / f"{new_file.file_id}.png")
    rgb_image = image.convert('RGB')
    rgb_image.save(input_path / f"{new_file.file_id}.pdf",  "PDF")

    await update.message.reply_document(document=open(str(input_path / f"{new_file.file_id}.pdf"), 'rb'), caption=f'Your image converted to PDF is ready!')
 
    os.remove(input_path / f"{new_file.file_id}.png")
    os.remove(str(input_path / f"{new_file.file_id}.pdf"))
    # update.message.reply_photo(open(ofile, 'rb'), caption="Your file is ready!") 
 


async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("/start", "Start the bot") 
     ])

 

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token("7830114682:AAFQBhX3lclz-9HR1C5FAsIuHO8zSOYcOKY")
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .post_init(post_init)
        .build()
    ) 
    application.add_handler(MessageHandler(filters.PHOTO, handle_bg_remove))    # application.add_handler(CommandHandler("convert", show_facts_menu, filters=user_filter))
  
 

    try:
         create_path(input_path)
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__)) 
        print("Error", traceback_str, e) 
        print('*******************************************************************')
 

    application.run_polling()
    # application.add_handler(CommandHandler("help", help_handle, filters=user_filter))

    #   application.add_handler(CommandHandler("balance", show_balance_handle, filters=user_filter))
    



if __name__ == "__main__":
    run_bot()

