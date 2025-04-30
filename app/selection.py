from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)

class VentanaSeleccion(QWidget):
    def __init__(self, parent=None, modo_funcion="", texto_nav="Seleccionar Odontograma", nav_pile=[]):
        super().__init__(parent)
        self.parent = parent
        self.modo_funcion = modo_funcion
        self.texto_nav = texto_nav
        self.setObjectName('VS')

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

        # NAVEGACIÓN
        nav_layout = QHBoxLayout()
        nav_button = QPushButton(f"< {nav_pile[len(nav_pile)-1]}")  # usa el texto dinámico aquí
        nav_button.setObjectName("NavButton")
        nav_button.clicked.connect(self.volver_a_cliente)
        nav_layout.addWidget(nav_button)
        nav_layout.addStretch()
        main_layout.addLayout(nav_layout)

        # CONTENIDO PRINCIPAL
        content_layout = QHBoxLayout()

        # COLUMNA DE BOTONES
        botones_layout = QVBoxLayout()
        self.opciones = [
            ("Odontograma Inicial", "inicial"),
            ("Odontograma de Tratamiento", "tratamiento"),
            ("Odontograma de Evolución", "evolucion")
        ]
        for texto_visible, modo_clave in self.opciones:
            # Usamos lambda para pasar parámetros a la función abrir_editor
            boton = QPushButton(texto_visible)
            boton.clicked.connect(lambda modo=modo_clave, texto_visible=texto_visible: self.abrir_editor(modo, texto_visible))
            botones_layout.addWidget(boton)

        content_layout.addLayout(botones_layout)

        # IMAGEN ODONTOGRAMA ESCALADA A 1000x700
        imagen = QLabel()
        ruta_imagen = get_resource_path("ODON.png")
        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen).scaled(1000, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            imagen.setPixmap(pixmap)
            imagen.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(imagen)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        self.aplicar_estilo()

    def abrir_editor(self, modo, texto_boton):
        """Cambia a la ventana de editor con los parámetros correctos."""
        self.parent.np.append(texto_boton)  # Agrega la opción al historial de navegación
        self.parent.abrir_editor(self.modo_funcion, texto_boton)  # Cambiar a la ventana de editor

    def volver_a_cliente(self):
        self.parent.np.pop()  # Elimina la última opción de navegación
        self.parent.volver_a_cliente()

    def aplicar_estilo(self):
        ruta_qss = os.path.join(os.path.dirname(__file__), "resources/estilos_selection.qss")
        if os.path.exists(ruta_qss):
            with open(ruta_qss, "r") as f:
                self.setStyleSheet(f.read())
