from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget, QLineEdit, QLabel, QGraphicsEllipseItem, QGraphicsRectItem, QFrame
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QImage, QFont, QFontMetrics
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QRectF
import os

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)


class DrawingScene(QGraphicsScene):
    def __init__(self, background_path=None, color=Qt.black):
        super().__init__()
        self.tool = "text"
        self.start_point = None
        self.annotations = []
        self.graphics_items = []
        self.text_to_insert = "Anotación"
        self.temp_item = None
        self.color = color  # Color del trazo

        # Cargar el fondo
        original_pixmap = QPixmap(background_path) if background_path and os.path.exists(background_path) else QPixmap(1000, 700)
        if original_pixmap.isNull():
            original_pixmap.fill(Qt.white)

        # Ajustar el tamaño de la escena al tamaño de la imagen
        self.background = original_pixmap.scaled(1000, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setSceneRect(0, 0, self.background.width(), self.background.height())  # Ajustamos la escena al tamaño de la imagen
        self.addPixmap(self.background)  # Añadimos la imagen de fondo
        self.setSceneRect(self.background.rect())  # Definimos el área de la escena para que tenga el tamaño de la imagen

    def save_image(self, path):
        # Crear una imagen del canvas completo, incluidas las anotaciones
        # Usamos una resolución más alta para la imagen
        image_width = self.sceneRect().width()
        image_height = self.sceneRect().height()

        # Crear la imagen con mayor resolución
        image = QImage(image_width * 2, image_height * 2, QImage.Format_ARGB32)  # Doblamos la resolución
        image.fill(Qt.transparent)  # Fondo transparente inicialmente
        painter = QPainter(image)
        self.render(painter, QRectF(0, 0, image_width * 2, image_height * 2))  # Renderiza toda la escena con la nueva resolución
        painter.end()

        image = image.scaled(image_width, image_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Escalar la imagen a su tamaño original
        image.save(path)  # Guardamos la imagen del canvas


    def set_tool(self, tool_name):
        self.tool = tool_name

    def set_text(self, new_text):
        self.text_to_insert = new_text.strip() if new_text.strip() else "Anotación"

    def set_color(self, color):
        self.color = color  # Cambiar el color del trazo

    def mousePressEvent(self, event):
        if self.tool == "text":
            font = QFont("Arial", 12)  # Cambié el tamaño de la fuente a 12 (más pequeño)
            text_item = self.addText(self.text_to_insert, font)
            text_item.setDefaultTextColor(self.color)  # Usar el color actual

            # Usar QFontMetrics para obtener el tamaño del texto
            font_metrics = QFontMetrics(font)
            text_width = font_metrics.horizontalAdvance(self.text_to_insert)  # Usar horizontalAdvance
            text_height = font_metrics.height()

            # Ajustar la posición para que el punto medio del texto esté donde haces clic
            x_pos = event.scenePos().x() - text_width / 2  # Desplazar el texto a la izquierda
            y_pos = event.scenePos().y() - text_height / 2  # Desplazar el texto hacia arriba

            text_item.setPos(x_pos, y_pos)  # Colocar el texto en la nueva posición
            self.graphics_items.append(text_item)
            self.annotations.append({
                "tipo": "texto",
                "x": x_pos,
                "y": y_pos,
                "texto": self.text_to_insert
            })
        else:
            self.start_point = event.scenePos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.start_point:
            return

        if self.tool == "brush":
            end = event.scenePos()
            pen = QPen(self.color, 2)  # Usar el color actual
            line = self.addLine(self.start_point.x(), self.start_point.y(), end.x(), end.y(), pen)
            self.graphics_items.append(line)
            self.annotations.append({
                "tipo": "pincel",
                "x1": self.start_point.x(), "y1": self.start_point.y(),
                "x2": end.x(), "y2": end.y()
            })
            self.start_point = end

        elif self.tool in ["line", "circle"]:
            if self.temp_item:
                self.removeItem(self.temp_item)

            end = event.scenePos()
            x1, y1 = self.start_point.x(), self.start_point.y()
            x2, y2 = end.x(), end.y()

            if self.tool == "line":
                pen = QPen(self.color, 2)  # Usar el color actual
                self.temp_item = self.addLine(x1, y1, x2, y2, pen)

            elif self.tool == "circle":
                pen = QPen(self.color, 2)  # Usar el color actual
                self.temp_item = QGraphicsEllipseItem(QRectF(x1, y1, x2 - x1, y2 - y1))
                self.temp_item.setPen(pen)
                self.addItem(self.temp_item)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self.start_point:
            return

        end = event.scenePos()
        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = end.x(), end.y()

        if self.temp_item:
            self.graphics_items.append(self.temp_item)
            self.temp_item = None

        if self.tool == "line":
            self.annotations.append({"tipo": "linea", "x1": x1, "y1": y1, "x2": x2, "y2": y2})
        elif self.tool == "circle":
            self.annotations.append({"tipo": "circulo", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

        self.start_point = None
        super().mouseReleaseEvent(event)

    def deshacer_ultima_anotacion(self):
        if self.graphics_items:
            item = self.graphics_items.pop()
            self.removeItem(item)
        if self.annotations:
            self.annotations.pop()

class OdontogramaEditor(QWidget):
    def __init__(self, modo="Modo Edición", modo_funcion="crear", texto_nav="Odontograma", parent=None, nav_pile=[]):
        super().__init__(parent)
        self.modo = modo
        self.modo_funcion = modo_funcion
        self.texto_nav = texto_nav
        self.parent = parent
        self.volver_callback = None
        self.current_color = Qt.blue  # Color inicial del trazo (azul por defecto)

        self.setWindowTitle("Editor de Odontograma")

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

        # BOTÓN DE NAVEGACIÓN
        nav_layout = QHBoxLayout()
        nav_button = QPushButton(f"← {nav_pile[len(nav_pile)-1]}")  # Usamos texto dinámico aquí
        nav_button.setObjectName("NavButton")
        nav_button.clicked.connect(self.volver_a_seleccion)  # Conecta al método de volver
        nav_layout.addWidget(nav_button)
        nav_layout.addStretch()
        main_layout.addLayout(nav_layout)

        # ZONA CENTRAL
        content_layout = QHBoxLayout()
        tools_layout = QVBoxLayout()
        tools = [("Línea", "line"), ("Círculo", "circle"), ("Pincel", "brush"),
                 ("Texto", "text"),
                 ("Deshacer", "undo"), ("Color Azul", "blue"), ("Color Rojo", "red"),("Guardar", "save")]  # Añadido "Color Azul" y "Color Rojo"

        for name, tool in tools:
            btn = QPushButton(name)
            if tool == "undo":
                btn.setObjectName("OB")
                btn.clicked.connect(self.deshacer_ultima_anotacion)
            elif tool == "save":
                btn.setObjectName("SB")
                btn.clicked.connect(self.guardar_imagen)
            elif tool == "blue":
                btn.setObjectName("OB")
                btn.clicked.connect(self.set_color_blue)  # Cambiar a azul
            elif tool == "red":
                btn.setObjectName("OB")
                btn.clicked.connect(self.set_color_red)  # Cambiar a rojo
            else:
                btn.setObjectName("OB")
                btn.clicked.connect(self._make_tool_callback(tool))
            tools_layout.addWidget(btn)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Texto para insertar...")
        self.text_input.returnPressed.connect(self.set_text_for_current_scene)
        tools_layout.addWidget(self.text_input)

        content_layout.addLayout(tools_layout)

        # CANVAS
        image_path = get_resource_path("ODON.png") if self.modo_funcion == "crear" else get_resource_path("antecedente.png")
        self.scene = DrawingScene(image_path, self.current_color)  # Pasar el color al constructor
        self.current_scene = self.scene
        view = QGraphicsView(self.scene)
        view.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(view, stretch=1)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.showMaximized()
        self.aplicar_estilo()

    def set_color_blue(self):
        self.current_color = Qt.blue  # Cambiar a azul
        self.current_scene.set_color(self.current_color)  # Cambiar el color en la escena

    def set_color_red(self):
        self.current_color = Qt.red  # Cambiar a rojo
        self.current_scene.set_color(self.current_color)  # Cambiar el color en la escena

    def volver_a_seleccion(self):
        self.parent.np.pop()
        self.close()
        self.parent.volver_a_seleccion("")  # Llama al método de la clase principal (MainApp)

    def aplicar_estilo(self):
        ruta_qss = get_resource_path("editor.qss")
        if os.path.exists(ruta_qss):
            with open(ruta_qss, "r") as f:
                self.setStyleSheet(f.read())

    def _make_tool_callback(self, tool_name):
        def set_tool():
            self.current_scene.set_tool(tool_name)
        return set_tool

    def set_text_for_current_scene(self):
        text = self.text_input.text()
        if self.current_scene:
            self.current_scene.set_text(text)

    def deshacer_ultima_anotacion(self):
        if self.current_scene:
            self.current_scene.deshacer_ultima_anotacion()
    
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        box = QMessageBox(self)
        box.setWindowTitle(titulo)
        box.setText(mensaje)
        
        if tipo == "info":
            box.setIcon(QMessageBox.Information)
        elif tipo == "error":
            box.setIcon(QMessageBox.Critical)
        
        # Estilo personalizado
        box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                color: #2E2D6D;
            }
            QPushButton {
                background-color: #2E2D6D;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4746a3;
            }
        """)
        box.exec()


    def guardar_imagen(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "PNG (*.png)")
        if file_name:
            try:
                self.current_scene.save_image(file_name)
                self.mostrar_mensaje("Éxito", "Imagen guardada exitosamente.", tipo="info")
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")
                self.mostrar_mensaje("Error", "Ocurrió un error al guardar la imagen. Intenta nuevamente.", tipo="error")



    def keyPressEvent(self, event):
        """Detecta cuando se presiona Ctrl+Z y deshace la última anotación."""
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            self.deshacer_ultima_anotacion()
