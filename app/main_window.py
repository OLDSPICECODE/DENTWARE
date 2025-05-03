import sys, os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame
from PySide6.QtGui import QFont

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)

class DentwareApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dentware - Centro Odontológico") # Ajusta el tamaño de la ventana

        # Número dinámico de pacientes (esto se puede cambiar según sea necesario)
        self.num_pacientes = 120  # Número simulado de pacientes

        # Layout principal
        main_layout = QHBoxLayout()  # Usamos QHBoxLayout para dividir la pantalla en dos partes
        left_layout = QVBoxLayout()  # Layout para la parte izquierda donde estarán los botones

        # Barra superior
        self.header_label = QLabel("Bienvenido a Dentware!")
        self.header_label.setObjectName("header_label")
        self.header_label.setAlignment(Qt.AlignLeft)
        self.header_label.setFont(QFont("Arial", 24, QFont.Bold))

        # Barra de búsqueda (más grande y centrada, un poco a la derecha)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar paciente")
        self.search_bar.setObjectName("search_bar")

        # Botones y estadísticas (botón de añadir paciente alineado a la izquierda)
        button_layout = QVBoxLayout()  # Usamos QVBoxLayout para apilar los botones verticalmente
        add_patient_button = QPushButton("+ Añadir paciente")
        add_patient_button.setObjectName("add_patient_button")
        add_patient_button.setStyleSheet("min-height: 15px;min-width:125px;max-height: 15px;max-width:125px;")
        
        # Convertir el número de pacientes en un botón
        patient_count_button = QPushButton(f"Pacientes: {self.num_pacientes}")
        patient_count_button.setObjectName("patient_count_button")
        patient_count_button.setStyleSheet("min-height: 15px;min-width:125px;max-height: 15px;max-width:125px;")
        
        # Añadir los botones al layout
        button_layout.addWidget(add_patient_button)
        button_layout.addWidget(patient_count_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Alineamos los botones hacia la parte superior

        # Contenedor con el fondo celeste para los botones
        button_container = QFrame()
        button_container.setObjectName("BC")
        button_container.setLayout(button_layout)
        button_container.setStyleSheet("background-color:   #c8d6f7;min-height: 900px; ")  # Celeste con opacidad

        # Layout para dividir la parte izquierda (botones) y derecha (barra de búsqueda)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(button_container)  # Parte izquierda con los botones
        hbox_layout.addWidget(self.search_bar)  # Parte derecha con la barra de búsqueda
        hbox_layout.setStretch(0, 1)  # Hacer que los botones ocupen más espacio
        hbox_layout.setStretch(1, 2)  # Hacer que la barra de búsqueda ocupe el doble de espacio que los botones

        # Agregar la barra superior y el layout de botones y búsqueda
        main_layout.addLayout(left_layout)
        left_layout.addWidget(self.header_label)
        left_layout.addLayout(hbox_layout)  # Agregar el layout con los botones y la barra de búsqueda

        # Crear un frame para contener todos los elementos
        container_frame = QFrame()
        container_frame.setLayout(main_layout)
        container_frame.setStyleSheet("background-color: #ffffff;")

        # Configuración de la interfaz
        self.setLayout(main_layout)
        
        # Cargar el archivo de estilo QSS
        self.aplicar_estilo()

    def aplicar_estilo(self):
        """Método para aplicar el archivo de estilo QSS"""
        ruta_qss = get_resource_path("app.qss")
        if os.path.exists(ruta_qss):
            with open(ruta_qss, "r") as f:
                self.setStyleSheet(f.read())

# Aplicación Qt
def main():
    app = QApplication(sys.argv)
    window = DentwareApp()
    window.show()
    return app.exec()

if __name__ == "__main__":
    main()
