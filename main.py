import sys
from PySide6.QtWidgets import QApplication
from app.editor import OdontogramaEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = OdontogramaEditor()
    ventana.resize(1000, 700)
    ventana.show()
    sys.exit(app.exec())
