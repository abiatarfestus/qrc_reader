import cv2
import winsound
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
from PyQt5.QtCore import QObject, pyqtSignal
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
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.capture.set(cv2.CAP_PROP_FOCUS, 100)
        while self.camera_on:
            try:
                ret, frame = self.capture.read()
                if ret:
                    # get_data() outputs a list qrc_data and an image/frame to coverted to QPixmap
                    frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    qrc_data, image = self.get_data(frame)
                    # change the image/video frame to QImage>QPixmap
                    qt_image = QImage(image, image.shape[1], image.shape[0], QImage.Format_BGR888)
                    qt_pixmap = QPixmap.fromImage(qt_image)
                    self.video_feed.emit(qt_pixmap)
                    # process the qrc_data
                    id_number = qrc_data[0].strip()
                    app_number = qrc_data[1]
                    name = qrc_data[2]
                    if len(id_number)==11:
                        self.id_numbers.add(id_number)
                        self.id_scanned.emit([id_number, app_number, name, len(self.id_numbers)])
            except Exception as e:
                self.str_message.emit(repr(e))
                self.thread_active = False
                break
        self.video_ended.emit("Waiting for video feed")
        self.finished.emit(self.id_numbers)
        self.capture.release()

    
    def get_data(self, image):
        id_number = ""
        app_number = ""
        name = ""
        try:
            image = cv2.cvtColor(image, 1)
            qrcode = decode(image, symbols=[ZBarSymbol.QRCODE])

            for obj in qrcode:
                qrc_data = obj.data.decode("utf-8")
                pts = np.array([obj.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 5)
                qrc_data_list = qrc_data.split(";")
                id_number = qrc_data_list[0]
                app_number = qrc_data_list[-1]
                name = f"{qrc_data_list[1]} {qrc_data_list[2]}"
                winsound.Beep(440, 500)
        except IndexError:
                pass
        except Exception as e:
            self.str_message.emit(repr(e))
            self.thread_active = False
        return [id_number, app_number, name], image