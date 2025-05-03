import sys, os
import psycopg2  # Usamos psycopg2 para conectarnos a PostgreSQL
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QScrollArea
from PySide6.QtGui import QFont
from app.db_config import obtener_conexion  # Asegúrate de que esta función esté correctamente definida

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)

class DentwareApp(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Dentware - Centro Odontológico")  # Ajusta el tamaño de la ventana
        self.parent = parent  # Guardamos una referencia al padre (VentanaCliente o el componente que lo llame)
        
        # Conectar a la base de datos PostgreSQL
        self.cnx = obtener_conexion()  # Llamamos a la función para obtener la conexión
        if self.cnx:
            print("Conexión a la base de datos establecida exitosamente en el editor")
        else:
            print("No se pudo establecer la conexión a la base de datos en el editor")

        # Número dinámico de pacientes (esto se puede cambiar según sea necesario)
        self.num_pacientes = 120  # Número simulado de pacientes

        # Layout principal
        main_layout = QHBoxLayout()  # Usamos QHBoxLayout para dividir la pantalla en dos partes
        left_layout = QVBoxLayout()  # Layout para la parte izquierda donde estarán los botones
        right_layout = QVBoxLayout()  # Layout para la parte derecha (barra de búsqueda y resultados)

        # Barra superior
        self.header_label = QLabel("Bienvenido a Dentware!")
        self.header_label.setObjectName("header_label")
        self.header_label.setAlignment(Qt.AlignLeft)
        self.header_label.setFont(QFont("Arial", 24, QFont.Bold))

        # Barra de búsqueda (más grande y centrada, un poco a la derecha)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar paciente")
        self.search_bar.setObjectName("search_bar")

        # Conectar la señal de texto cambiado a la función de búsqueda
        self.search_bar.textChanged.connect(self.buscar_paciente)

        # Botones y estadísticas
        button_layout = QVBoxLayout()  # Usamos QVBoxLayout para apilar los botones verticalmente
        add_patient_button = QPushButton("+ Añadir paciente")
        add_patient_button.setObjectName("add_patient_button")
        add_patient_button.setStyleSheet("background-color: white; min-height: 15px; min-width: 125px; max-height: 15px; max-width: 125px; border: 2px solid #1E2A5A;")
        
        patient_count_button = QPushButton(f"Pacientes: {self.num_pacientes}")
        patient_count_button.setObjectName("patient_count_button")
        patient_count_button.setStyleSheet("background-color: white; min-height: 15px; min-width: 125px; max-height: 15px; max-width: 125px; border: 2px solid #1E2A5A;")

        button_layout.addWidget(add_patient_button)
        button_layout.addWidget(patient_count_button)
        button_layout.setAlignment(Qt.AlignTop)

        # Contenedor con fondo celeste para los botones
        button_container = QFrame()
        button_container.setObjectName("BC")
        button_container.setLayout(button_layout)
        button_container.setStyleSheet("background-color: #c8d6f7; padding: 20px; border-radius: 10px; min-height: 900px;")

        # Layout para dividir la parte izquierda (botones) y derecha (barra de búsqueda y resultados)
        left_layout.addWidget(self.header_label)
        left_layout.addWidget(button_container)

        # Crear un área de desplazamiento para los resultados de búsqueda
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(QFrame())  # Un contenedor vacío de base para los resultados
        self.scroll_layout = QVBoxLayout(self.scroll_area.widget())
        self.scroll_area.setFixedHeight(300)  # Establece un tamaño fijo para la zona de resultados

        # Colocamos la barra de búsqueda y los resultados dentro de la parte derecha
        right_layout.addWidget(self.search_bar)  # Barra de búsqueda
        right_layout.addWidget(self.scroll_area)  # Resultados de búsqueda

        # Agregar layouts a la ventana principal
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)  # Parte derecha con búsqueda y resultados

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

    def buscar_paciente(self):
        """Realizar la consulta a la base de datos cuando el texto en la barra de búsqueda cambie"""
        query_text = self.search_bar.text()
        
        cursor = self.cnx.cursor()
        
        # Consulta SQL para buscar pacientes por nombre, apellido o DNI (modificado para PostgreSQL)
        query = """
            SELECT nombres, apellidos, paciente_dni 
            FROM paciente
            WHERE nombres ILIKE %s OR apellidos ILIKE %s OR paciente_dni ILIKE %s
        """
        cursor.execute(query, (f"%{query_text}%", f"%{query_text}%", f"%{query_text}%"))

        # Limpiar los resultados previos
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Mostrar los resultados como snippets en la interfaz
        results = cursor.fetchall()
        print("Resultados de la búsqueda:")
        for result in results:
            nombre, apellido, dni = result
            patient_widget = self.create_patient_widget(nombre, apellido, dni)
            self.scroll_layout.addWidget(patient_widget)

    def create_patient_widget(self, nombre, apellido, dni):
        """Crear un botón para cada paciente que incluye nombre, apellido y DNI"""
        # Crear un botón para cada paciente con nombre, apellido y DNI
        patient_button = QPushButton(f"{nombre} {apellido} - DNI: {dni}")
        patient_button.setStyleSheet("background-color: #c8d6f7; padding: 10px; border-radius: 10px; margin: 5px;")
        
        # Conectar el clic del botón a la función 'volver_a_cliente' del padre
        patient_button.clicked.connect(lambda: self.parent.volver_a_cliente())

        return patient_button


# Aplicación Qt
def main():
    app = QApplication(sys.argv)
    window = DentwareApp()
    window.show()
    return app.exec()

if __name__ == "__main__":
    main()
