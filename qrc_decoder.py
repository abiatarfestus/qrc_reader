import cv2
import winsound
import numpy as np
from datetime import datetime
from pyzbar.pyzbar import decode, ZBarSymbol

timestamp_ = int(datetime.timestamp(datetime.now()))
file_name = f"Inventory_{timestamp_}.csv"


def decoder(image):
    gray_img = cv2.cvtColor(image, 1)
    qrcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])
    id_number = ""

    for obj in qrcode:
        qrcodeData = obj.data.decode("utf-8")
        id_number = qrcodeData[:11]
        winsound.Beep(440, 500)
        print(id_number)
    return id_number


id_numbers = set()
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    id_ = decoder(gray_frame)
    if len(id_) == 11:
        id_numbers.add(id_)
    cv2.imshow("Image", gray_frame)
    code = cv2.waitKey(1)
    if code == ord("q"):
        break

np.savetxt(file_name, list(id_numbers), delimiter=", ", fmt="% s")
print("After camera closed:", id_numbers)
cv2.destroyAllWindows()
cap.release()

# https://stackoverflow.com/questions/67886525/got-this-error-on-my-pyzbar-program-after-i-converted-to-exe-with-pyinstaller
# pyinstaller --onefile --add-binary "C:\Users\Festus Abiatar\AppData\Local\Programs\Python\Python39\Lib\site-packages\pyzbar\
# libiconv.dll;pyzbar" --add-binary "C:\Users\Festus Abiatar\AppData\Local\Programs\Python\Python39\Lib\site-packages\pyzbar\
# libzbar-64.dll;pyzbar" qrc_decoder.py

# pyinstaller -w --add-binary "C:\Users\abiat\OneDrive\Documents\My Code\qrc_reader\.env\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "C:\Users\abiat\OneDrive\Documents\My Code\qrc_reader\.env\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" main.py
