import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app.cliente import VentanaCliente
from app.selection import VentanaSeleccion
from app.editor import OdontogramaEditor

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DENTWARE")
        self.np = []  # Pila de navegación
        self.func = ""
        self.ventana_cliente = VentanaCliente(parent=self, nav_pile=self.np)
        self.setCentralWidget(self.ventana_cliente)
        self.showMaximized()
        self.setStyleSheet("background-color:white")

    def volver_a_cliente(self):
        self.ventana_cliente = VentanaCliente(parent=self, nav_pile=self.np)
        self.setCentralWidget(self.ventana_cliente)
    
    def volver_a_seleccion(self, texto_nav):
        self.ventana_cliente = VentanaSeleccion(parent=self, modo_funcion=self.func, texto_nav=texto_nav, nav_pile=self.np)
        self.setCentralWidget(self.ventana_cliente)

    def abrir_seleccion(self, texto_nav):
        self.ventana_seleccion = VentanaSeleccion(parent=self, modo_funcion=self.func, texto_nav=texto_nav, nav_pile=self.np)
        self.setCentralWidget(self.ventana_seleccion)

    def abrir_editor(self, modo, texto_nav):
        self.editor = OdontogramaEditor(modo=modo, modo_funcion=self.func, texto_nav=texto_nav, parent=self, nav_pile=self.np)
        self.setCentralWidget(self.editor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainApp()
    ventana.show()
    sys.exit(app.exec())
    