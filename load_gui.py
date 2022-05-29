import os
from PyQt5.uic import loadUi
from numpy import choose
from db import (
    setup_db,
    create_connection,
    create_office,
    create_location,
    select_office,
    select_location,
    update_office,
    update_location
)
from functools import partial
from popups import display_message
from worker_thread import Worker
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

setup_db()

class OfficeDialog(QDialog):
    office_updated = pyqtSignal()
    def __init__(self, rowid=0, record=None):
        super(OfficeDialog, self).__init__()
        loadUi("office_form.ui", self)
        self.setWindowTitle("Office Form")
        self.rowid = rowid
        self.row_id.setEnabled(False)
        if rowid == 0:
            self.rbtn_update_office.setCheckable(False)
            self.lbl_office_form_heading.setText("Add a New Office to the Database")
            self.rbtn_create_office.setChecked(True)
            self.btn_create.setText("Add")
        else:
            self.rbtn_create_office.setCheckable(False)
            self.lbl_office_form_heading.setText("Update an Office in the Database")
            self.rbtn_update_office.setChecked(True)
            self.row_id.setText(str(rowid))
            self.office_name.setText(record[1])
            self.btn_create.setText("Update")
        self.btn_create.clicked.connect(self.create_update_office)
        self.btn_cancel.clicked.connect(self.close)
        # self.rbtn_create_office.toggled.connect(self.force_create)

    def create_update_office(self):
        office_name = self.office_name.text().strip()
        conn = create_connection("mydb.db")
        if self.rbtn_create_office.isChecked():
            if create_office(conn, (office_name,)):
                # self.reset()
                self.close()
        else:
            rowid = int(self.row_id.text())
            if display_message("confirm_update") == QMessageBox.Yes:
                if update_office(conn, (office_name, rowid)):
                    # self.rbtn_create_office.setChecked(True)
                    self.close()
        self.office_updated.emit()
        return

    # def reset(self):
    #     self.office_name.setText("")
    #     self.row_id.setText("")
    #     self.btn_create.setText("Add")
    #     self.lbl_office_form_heading.setText("Add a New Office to the Database")

    # def force_create(self):
    #     self.reset()
    #     self.rbtn_update_office.setCheckable(False)

class LocationDialog(QDialog):
    location_updated = pyqtSignal()
    def __init__(self, rowid=0, record=None):
        super(LocationDialog, self).__init__()
        loadUi("location_form.ui", self)
        self.setWindowTitle("Location Form")
        self.rowid = rowid
        self.location_path = None
        self.row_id.setEnabled(False)
        self.txt_location_path.setEnabled(False)
        if rowid == 0:
            self.rbtn_update_location.setCheckable(False)
            self.lbl_location_form_heading.setText("Add a New Location to the Database")
            self.rbtn_create_location.setChecked(True)
            self.btn_create.setText("Add")
        else:
            self.rbtn_create_location.setCheckable(False)
            self.lbl_location_form_heading.setText("Update a Location in the Database")
            self.rbtn_update_location.setChecked(True)
            self.row_id.setText(str(rowid))
            self.txt_location_path.setText(record[1])
            self.btn_create.setText("Update")
        self.btn_choose_location.clicked.connect(self.choose_folder)
        self.btn_create.clicked.connect(self.create_update_location)
        self.btn_cancel.clicked.connect(self.close)
        # self.rbtn_create_location.toggled.connect(self.force_create)

    def choose_folder(self):
        output_folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.txt_location_path.setText(output_folder_path)
        # print(f"OUTPUT: {output_folder_path}")
        return


    def create_update_location(self):
        if self.txt_location_path:
            self.location_path = self.txt_location_path.text()
            conn = create_connection("mydb.db")
            if self.rbtn_create_location.isChecked():
                if create_location(conn, (self.location_path,)):
                    # self.reset()
                    self.close()
            else:
                rowid = int(self.row_id.text())
                if display_message("confirm_update") == QMessageBox.Yes:
                    if update_location(conn, (self.location_path, rowid)):
                        # self.rbtn_create_location.setChecked(True)
                        self.close()
        self.location_updated.emit()
        return

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.camera_on = False
        self.office = self.cbx_office.currentText()
        self.location = self.cbx_location.currentText()
        self.btn_exit.clicked.connect(self.exit_app)
        self.btn_update_office.clicked.connect(self.add_update_office)
        self.btn_update_location.clicked.connect(self.add_update_location)
        self.btn_launch_camera.clicked.connect(self.set_camera_button_function)
        self.btn_generate_file.clicked.connect(self.generate_file)
        self.cbx_office.currentIndexChanged.connect(self.set_office)
        self.cbx_location.currentIndexChanged.connect(self.set_location)
        self.load_offices()
        self.load_locations()
        # self.load_video_frame()

    def set_camera_button_function(self, function=None):
        if self.camera_on:
            function()
        else:
            self.launch_camera()

    def update_scanned(self, vars):
        self.lbl_id_number.setText(vars[0])
        self.lbl_application_number.setText(vars[1])
        self.lbl_name.setText(vars[2])
        self.lc_total_scanned.display(vars[3])
    
    def reset_scanned(self):
        self.lbl_id_number.setText('None')
        self.lbl_application_number.setText('None')
        self.lbl_name.setText('None')
        self.lcd_total_scanned.display(0)

    def load_locations(self):
        conn = create_connection("mydb.db")
        location = select_location(conn)
        self.cbx_location.clear()
        if location:
            self.cbx_location.addItem(location[1])

    def load_offices(self):
        conn = create_connection("mydb.db")
        office = select_office(conn)
        self.cbx_office.clear()
        if office:
            self.cbx_office.addItem(office[1])

    def set_location(self):
        self.office = self.cbx_office.currentText()
        return

    def set_office(self):
        self.office = self.cbx_office.currentText()
        return

    def video_feed(self, image):
        try:
            self.lbl_video_feed.setPixmap(image)
        except Exception as e:
                display_message(repr(e))
        
    def generate_file(self):
        if self.camera_on:
            display_message("Your camera seems to be running. Click Stop Video and try again.")
        else:
            print("GENERATING Excel File...")
        return

    def video_stopped(self):
        self.camera_on = False
        self.btn_launch_camera.setText("Launch Camera")
        self.btn_launch_camera.clicked.connect(self.launch_camera)
        self.lbl_video_feed.setText("Waiting for video feed")

    def add_update_office(self):
        conn = create_connection("mydb.db")
        record = select_office(conn)
        if record == None:
            rowid = 0
        else:
            rowid = record[0]
        self.office_dialog = OfficeDialog(rowid, record)
        self.office_dialog.office_updated.connect(self.load_offices)
        self.office_dialog.show()

    def add_update_location(self):
        conn = create_connection("mydb.db")
        record = select_location(conn)
        if record == None:
            rowid = 0
        else:
            rowid = record[0]
        self.location_dialog = LocationDialog(rowid, record)
        self.location_dialog.location_updated.connect(self.load_locations)
        self.location_dialog.show()

    def launch_camera(self):
        if  display_message("confirm_reset") == QMessageBox.Yes:
            self.camera_on = True
            self.btn_launch_camera.setText("Stop Video")
            self.reset_scanned()
            self.thread = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.video_feed.connect(self.video_feed)
            self.worker.id_scanned.connect(self.update_scanned)
            self.btn_launch_camera.clicked.connect(self.worker.stop_video)
            self.worker.str_message.connect(display_message)
            self.worker.finished.connect(self.video_stopped)
            self.worker.finished.connect(self.thread.quit)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.start()
        return

    def exit_app(self):
        if display_message("confirm_exit") == QMessageBox.Yes:
            QCoreApplication.instance().quit()