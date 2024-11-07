import cv2
from pyzbar.pyzbar import decode
from PIL import Image

def scan():
    qrcode_filename = "C:\\Users\\syske\\Desktop\\Snipaste_2024-08-29_17-20-04.png"
    qrcode_image = cv2.imread(qrcode_filename)
    qrCodeDetector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
    print(data, bbox, straight_qrcode)

def scan2():
    decocdeQR = decode(Image.open("C:\\Users\\syske\\Desktop\\Snipaste_2024-08-29_17-20-04.png"))
    print(decocdeQR[0].data.decode('ascii'))


scan2()
