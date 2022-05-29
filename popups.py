from PyQt5.QtWidgets import QMessageBox


def display_message(message, office=None, path=None, record=None, file_name=""):
    if message == "confirm_process":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Process")
        msg.setText(
            f"This process will generate an excel file of scanned ID for {office} and save it at this location: \n{path}"
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_update":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Update")
        msg.setText(
            "This operation will modify the selected database record."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_delete":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(
            f"This operation will delete {record} from the database."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_reset":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Reset")
        msg.setText(
            f"This operation will start a new session. All ID numbers already scanned but not yet saved to the Excel file will be lost."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_exit":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Exit")
        msg.setText(
            f"You're about to close the App. All ID numbers scanned but not saved to the Excel file will be lost."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif type(message) == int:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText(f"An Excel file {file_name} was successfully created at this location:\n{path}")
        msg.setInformativeText("Verify the file and upload to NPRS")
        msg.exec_()
    elif message == "no_file":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Either the file, month or office is not selected for processing!")
        msg.setInformativeText("Please ensure that you've selected the file with payslips, the office and the pay month.")
        msg.exec_()
    elif message == "success_update":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully updated!")
        msg.exec_()
    elif message == "success_create":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully created!")
        msg.exec_()
    elif message == "success_delete":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully deleted!")
        msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Oops! Something went wrong!")
        msg.setDetailedText(message)
        msg.exec_()