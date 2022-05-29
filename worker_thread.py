import cv2
import winsound
import numpy as np
from datetime import datetime
from popups import display_message
from pyzbar.pyzbar import decode, ZBarSymbol
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class Worker(QObject):
    id_scanned = pyqtSignal(list)
    finished = pyqtSignal()
    video_feed = pyqtSignal(QPixmap)
    str_message = pyqtSignal(str)

    def __init__(self):
        super(Worker, self).__init__()
        self.scan_count = 0
        self.id_numbers = set()
        # self.timestamp_ = int(datetime.timestamp(datetime.now()))
        # self.file_name = f'Inventory_{self.timestamp_}.csv'
        self.thread_active = True

    def run(self):
        self.capture = cv2.VideoCapture(0)
        while self.thread_active:
            try:
                ret, frame = self.capture.read()
                if ret:
                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    qt_image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    qt_pixmap = QPixmap.fromImage(qt_image)
                    self.video_feed.emit(qt_pixmap)
                    id_number = self.get_data(frame)
                    if id_number:
                        self.id_numbers.add(id_number)
                        self.scan_count += 1
            except Exception as e:
                self.str_message.emit(repr(e))
                break
        # cv2.destroyAllWindows()
        self.finished.emit()
        self.capture.release()

    
    def get_data(self, image):
        try:
            gray_img = cv2.cvtColor(image, 1)
            qrcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

            for obj in qrcode:
                qrcodeData = obj.data.decode("utf-8")
                id_number = qrcodeData[:11]
                app_number = "App_num"
                name = "Name"
                winsound.Beep(440, 500)
                if len(id_number) == 11:
                    print(id_number, app_number, name, self.scan_count)
                    self.id_scanned.emit([id_number, app_number, name, self.scan_count])
                    return id_number
                else:
                    return None
        except Exception as e:
            display_message(repr(e))
            return None
        
    
    def stop_video(self):
        self.thread_active = False
        # self.finished.emit()
