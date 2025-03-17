import qrcode
import cv2

def generate_QR():
    data = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)

    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red', back_color = 'white')

    img.save('SuperSecretData.png')

def read_QR():
    image_name = "SuperSecretData.png"
    qr_image = cv2.imread(image_name)
    qr_detector = cv2.QRCodeDetector()

    data, vertices_array, binary_qrcode = qr_detector.detectAndDecode(qr_image)

    if vertices_array is not None:
        print("QRCode data:")
        print(data)
    else:
        print("There was some error") 

if __name__ == "__main__":
    # generate_QR()
    read_QR()