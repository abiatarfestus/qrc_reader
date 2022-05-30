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
                    qrc_data = self.get_data(frame)
                    id_number = qrc_data[0].strip()
                    app_number = qrc_data[1]
                    name = qrc_data[2]
                    if len(id_number)==11:
                        print(id_number, app_number, name, len(self.id_numbers))
                        self.id_numbers.add(id_number)
                        self.id_scanned.emit([id_number, app_number, name, len(self.id_numbers)])
            except Exception as e:
                self.str_message.emit(repr(e))
                self.thread_active = False
                break
        # cv2.destroyAllWindows()
        self.finished.emit()
        self.capture.release()

    
    def get_data(self, image):
        id_number = ""
        app_number = ""
        name = ""
        try:
            gray_img = cv2.cvtColor(image, 1)
            qrcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

            for obj in qrcode:
                qrc_data = obj.data.decode("utf-8")
                print(f"FULL_DATA: {qrc_data}")
                id_number = qrc_data[:11]
                app_number = "App_num"
                name = "Name"
                winsound.Beep(440, 500)
        except Exception as e:
            self.str_message.emit(repr(e))
            self.thread_active = False
        return [id_number, app_number, name]
        
        
    
    def stop_video(self):
        self.thread_active = False
        # self.finished.emit()
