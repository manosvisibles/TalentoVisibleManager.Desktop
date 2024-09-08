import sys, os
from utils import Config, DbManager, GSpreadSheet
from controllers import MainWindowController

from PySide6 import QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile, QIODevice, QCoreApplication

def show_error_dialog(message: str):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.setStandardButtons(QMessageBox.Ok)
    if error_dialog.exec() == QMessageBox.Ok:
        QCoreApplication.quit()
        sys.exit()

if __name__ == "__main__":
    config = Config()
    db_manager = DbManager()

    font_dpi = config.get("FONT_DPI")
    if font_dpi is not None or font_dpi != "":
        print(f"[ENVIRONMENT] Setting QT_FONT_DPI to {font_dpi}")
        os.environ["QT_FONT_DPI"] = str(font_dpi)

    sheet_id = config.get("MASTER_SHEET_ID")
    range_name = config.get("MASTER_SHEET_RANGE")
    master_sheet = GSpreadSheet(sheet_id, range_name, readonly=False)
    db_manager.set_gspreadsheet(master_sheet)
    db_manager.synchronize()

    QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    style = config.get("APPLICATION_STYLE")
    if style is not None and style.strip():
        app.setStyle(style)

    ui_file_name = "ui/main_window.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    window.setFixedSize(window.size())
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    controller = MainWindowController(window, db_manager)

    sys.exit(app.exec())
