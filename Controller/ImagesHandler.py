import os, qrcode, cv2, random
from telegram import Update
from telegram.ext import ContextTypes
#Función para obtener y leer un código QR a partir de una imagen enviada por Telegram
async def get_qr_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Obtenemos la imagen más reciente enviada
        photo = update.effective_message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # Definimos la ruta para guardar la imagen
        output_path = f"./Images/SuperSecretData-{context._user_id}.jpg"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Descargamos la imagen localmente
        await file.download_to_drive(output_path)
        # Intentamos leer el QR desde la imagen descargada
        return read_QR(output_path)
    except:
        print('An exception fetching the images from telegram occurred')

# 🧾 Función para generar un código QR a partir de una cadena de texto
def generate_QR(data: str, name: str, qr_type: str):
    # data = "https://www.youtube.com/shorts/SXHMnicI6Pg"
    # Creamos la instancia del generador QR
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)
    # Insertamos los datos dentro del QR
    qr.add_data(data)
    qr.make(fit = True)
    # Configuramos los colores y generamos la imagen
    color= 'red' if qr_type == "QrForCar" else 'blue' 

    img = qr.make_image(fill_color = color, back_color = 'white')
    
    # Guardamos el archivo localmente con un nombre aleatorio
    """Esto permite usar fácilmente ese archivo en otras partes del 
    programa (por ejemplo, para mandarlo al usuario o para guardarlo en 
    base de datos)."""
    file_name=f'./Images/SuperSecretData-{name}={int(random.uniform(1,999)) }.jpg'
    img.save(file_name)
    return file_name

def read_QR(file_name: str):
    print(f"📂 Intentando leer QR desde: {file_name}")
    image_name = file_name

    print("Ruta absoluta:", os.path.abspath(file_name))
    print("¿Existe el archivo?", os.path.exists(file_name))
    qr_image = cv2.imread(image_name)
    if qr_image is None:
        print("❌ No se pudo abrir la imagen. Verifica la ruta o el nombre del archivo.")
        return None

    #qr_image = cv2.imread(image_name)

    qr_detector = cv2.QRCodeDetector()

    data, vertices_array, binary_qrcode = qr_detector.detectAndDecode(qr_image)

    if vertices_array is not None:
        print(f"✅ QRCode data: {data}")
    else:
        print("⚠️ No se detectó ningún código QR en la imagen.")
    return data

if __name__ == "__main__":
    #generate_QR("{nombre: 'Mario', edad: '27'}")
    read_QR("../Images/SuperSecretData-5012562238=500.jpg")

