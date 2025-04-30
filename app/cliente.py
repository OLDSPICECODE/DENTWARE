from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

from app.selection import VentanaSeleccion

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)

class VentanaCliente(QWidget):
    def __init__(self, parent=None,nav_pile=[]):
        super().__init__(parent)
        self.parent = parent

        main_layout = QVBoxLayout()

        # HEADER
        header_layout = QHBoxLayout()
        logo = QLabel()
        logo_path = get_resource_path("logo.png")
        if os.path.exists(logo_path):
            logo.setPixmap(QPixmap(logo_path).scaledToHeight(40, Qt.SmoothTransformation))
        header_layout.addWidget(logo)

        title = QLabel("Concha Asociados\nCENTRO ODONTOLÓGICO")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # LÍNEA AZUL
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet("background-color: #2E2D6D; height: 2px;")
        main_layout.addWidget(linea)

        # SOLO 3 OPCIONES
        btn_crear = QPushButton("Crear Odontograma")
        btn_crear.clicked.connect(lambda: self.abrir_seleccion("crear", "Crear odontograma"))
        main_layout.addWidget(btn_crear)

        btn_actualizar = QPushButton("Actualizar Odontograma")
        btn_actualizar.clicked.connect(lambda: self.abrir_seleccion("actualizar", "Actualizar odontograma"))
        main_layout.addWidget(btn_actualizar)

        btn_visualizar = QPushButton("Visualizar Odontograma")
        btn_visualizar.clicked.connect(lambda: self.abrir_seleccion("visualizar", "Visualizar odontograma"))
        main_layout.addWidget(btn_visualizar)

        self.setLayout(main_layout)
        self.aplicar_estilo()

    def abrir_seleccion(self, modo_funcion, texto_nav):
        self.parent.func = modo_funcion
        self.parent.np.append(texto_nav)
        self.parent.abrir_seleccion(texto_nav)

    def aplicar_estilo(self):
        ruta_qss = os.path.join(os.path.dirname(__file__), "resources/estilos.qss")
        if os.path.exists(ruta_qss):
            with open(ruta_qss, "r") as f:
                self.setStyleSheet(f.read())
