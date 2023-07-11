import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from load_gui import MainWindow

# ====================================LOAD APPLICATION=======================================#
app = QApplication(sys.argv)
app.setApplicationName("ID Inventory Tool v1.1")
app.setStyle("Fusion")
home = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(661)
widget.setFixedWidth(967)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

# https://stackoverflow.com/questions/67886525/got-this-error-on-my-pyzbar-program-after-i-converted-to-exe-with-pyinstaller
# pyinstaller -w --add-binary "C:\Users\festus.abiatar\OneDrive\Code\qrc_reader\venv\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "C:\Users\festus.abiatar\OneDrive\Code\qrc_reader\venv\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" main.py
