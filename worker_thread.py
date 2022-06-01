import cv2
import winsound
import numpy as np
from datetime import datetime
from popups import display_message
from pyzbar.pyzbar import decode, ZBarSymbol
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPixmap


class Worker(QObject):
    id_scanned = pyqtSignal(list)
    finished = pyqtSignal(set)
    video_feed = pyqtSignal(QPixmap)
    video_ended = pyqtSignal(str)
    str_message = pyqtSignal(str)
    camera_on = None

    def __init__(self):
        super(Worker, self).__init__()
        self.id_numbers = set()

    def run(self):
        self.capture = cv2.VideoCapture(0)
        while self.camera_on:
            try:
                ret, frame = self.capture.read()
                if ret:
                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    qt_image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
                    qt_pixmap = QPixmap.fromImage(qt_image)
                    self.video_feed.emit(qt_pixmap)
                    qrc_data = self.get_data(frame)
                    id_number = qrc_data[0].strip()
                    app_number = qrc_data[1]
                    name = qrc_data[2]
                    if len(id_number)==11:
                        # print(id_number, app_number, name, len(self.id_numbers))
                        self.id_numbers.add(id_number)
                        self.id_scanned.emit([id_number, app_number, name, len(self.id_numbers)])
            except Exception as e:
                self.str_message.emit(repr(e))
                self.thread_active = False
                break
        # cv2.destroyAllWindows()\
        self.video_ended.emit("Waiting for video feed")
        self.finished.emit(self.id_numbers)
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
                # print(f"FULL_DATA: {qrc_data}")
                qrc_data_list = qrc_data.split(";")
                # print(f"FULL_DATA_LIST: {qrc_data_list}")
                id_number = qrc_data_list[0]
                app_number = qrc_data_list[-1]
                name = f"{qrc_data_list[1]} {qrc_data_list[2]}"
                winsound.Beep(440, 500)
        except Exception as e:
            self.str_message.emit(repr(e))
            self.thread_active = False
        return [id_number, app_number, name]
        
    
    # def stop_video(self):
    #     self.thread_active = False
        # self.finished.emit()
