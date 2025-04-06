import os, qrcode, cv2, random
from telegram import Update
from telegram.ext import ContextTypes

async def get_qr_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.effective_message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        output_path = f"./Images/SuperSecretData-{context._user_id}.jpg"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        await file.download_to_drive(output_path)
        return read_QR(output_path)
    except:
        print('An exception fetching the images from telegram occurred')

def generate_QR(data: str, name: str):
    # data = "https://www.youtube.com/shorts/SXHMnicI6Pg"
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)

    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black', back_color = 'white')

    img.save(f'./Images/SuperSecretData-{name}={int(random.uniform(1,999)) }.jpg')

def read_QR(file_name: str):
    image_name = file_name
    qr_image = cv2.imread(image_name)

    qr_detector = cv2.QRCodeDetector()

    data, vertices_array, binary_qrcode = qr_detector.detectAndDecode(qr_image)

    if vertices_array is not None:
        print(f"QRCode data: {data}")
    else:
        print("There was some error") 

    return data

if __name__ == "__main__":
    generate_QR("{nombre: 'Mario', edad: '27'}")
    read_QR("./Images/SuperSecretData-629917593.jpg")

