import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app.main_window import DentwareApp  # Importamos DentwareApp desde el archivo dentware_app.py
from app.cliente import VentanaCliente
from app.selection import VentanaSeleccion
from app.editor import OdontogramaEditor

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DENTWARE")
        self.np = []  # Pila de navegación
        self.func = ""  # Función de la app (para controlar el modo de operación)

        # Instanciar la pantalla de DentwareApp (Ventana principal de la app)
        self.dentware_app = DentwareApp(parent=self)

        # Establecer DentwareApp como el widget central de la ventana principal
        self.setCentralWidget(self.dentware_app)

        # Mostrar la ventana maximizada
        self.showMaximized()
        self.setStyleSheet("background-color:white")  # Estilo de fondo de la ventana

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
    
    # Crear la ventana principal
    ventana = MainApp()
    ventana.show()  # Mostrar la ventana principal
    
    sys.exit(app.exec())  # Iniciar el loop de la aplicación
