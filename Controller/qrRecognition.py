import qrcode
import cv2

def generate_QR():
    # data = "https://www.youtube.com/shorts/SXHMnicI6Pg"
    data = "{nombre: 'Mario', edad: '28'}"
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)

    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red', back_color = 'white')

    img.save('./Images/SuperSecretData.jpg')
    # img.save('./../Images/SuperSecretData.png')

def read_QR(file_name: str):
    # image_name = "./Images/SuperSecretData.jpg"
    image_name = file_name
    qr_image = cv2.imread(image_name)
    qr_detector = cv2.QRCodeDetector()

    data, vertices_array, binary_qrcode = qr_detector.detectAndDecode(qr_image)

    if vertices_array is not None:
        print(f"QRCode data: {data}")
    else:
        print("There was some error") 

if __name__ == "__main__":
    generate_QR()
    read_QR()