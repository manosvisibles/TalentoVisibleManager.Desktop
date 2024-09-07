import sys, os
from utils import Config, DbManager, GSpreadSheet
from controllers import MainWindowController

from PySide6 import QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, QCoreApplication

if __name__ == "__main__":

    config = Config()
    db_manager = DbManager()

    sheet_id = config.get("MASTER_SHEET_ID")
    range_name = config.get("MASTER_SHEET_RANGE")
    master_sheet = GSpreadSheet(sheet_id, range_name, readonly=False)

    db_manager.sync_with_gspreadsheet(master_sheet)

    font_dpi = config.get("FONT_DPI")
    if font_dpi is not None or font_dpi != "":
        os.environ["QT_FONT_DPI"] = font_dpi

    QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

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
    window.setWindowTitle("Banco hojas de vida")
    window.show()

    sys.exit(app.exec())
