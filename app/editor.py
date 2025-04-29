import os
from PySide6.QtWidgets import (
    QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QFileDialog,
    QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QGraphicsEllipseItem, QGraphicsRectItem
)
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QImage
from PySide6.QtCore import Qt, QRectF


def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "resources", filename)


class DrawingScene(QGraphicsScene):
    def __init__(self, background_path=None):
        super().__init__()
        self.tool = "line"
        self.start_point = None
        self.annotations = []
        self.graphics_items = []
        self.temp_item = None

        original_pixmap = QPixmap(background_path) if background_path and os.path.exists(background_path) else QPixmap(800, 400)
        if original_pixmap.isNull():
            original_pixmap.fill(Qt.white)

        self.background = original_pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.addPixmap(self.background)
        self.setSceneRect(self.background.rect())

    def set_tool(self, tool_name):
        self.tool = tool_name

    def mousePressEvent(self, event):
        self.start_point = event.scenePos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.start_point:
            return

        if self.tool == "brush":
            end = event.scenePos()
            pen = QPen(Qt.black, 2)
            line = self.addLine(self.start_point.x(), self.start_point.y(), end.x(), end.y(), pen)
            self.graphics_items.append(line)
            self.annotations.append({
                "tipo": "pincel",
                "x1": self.start_point.x(), "y1": self.start_point.y(),
                "x2": end.x(), "y2": end.y()
            })
            self.start_point = end

        elif self.tool in ["line", "circle", "highlight"]:
            if self.temp_item:
                self.removeItem(self.temp_item)

            end = event.scenePos()
            x1, y1 = self.start_point.x(), self.start_point.y()
            x2, y2 = end.x(), end.y()

            if self.tool == "line":
                pen = QPen(Qt.blue, 2)
                self.temp_item = self.addLine(x1, y1, x2, y2, pen)

            elif self.tool == "circle":
                pen = QPen(Qt.red, 2)
                self.temp_item = QGraphicsEllipseItem(QRectF(x1, y1, x2 - x1, y2 - y1))
                self.temp_item.setPen(pen)
                self.addItem(self.temp_item)

            elif self.tool == "highlight":
                color = QColor(255, 255, 0, 80)
                brush = QBrush(color)
                self.temp_item = QGraphicsRectItem(QRectF(x1, y1, x2 - x1, y2 - y1))
                self.temp_item.setBrush(brush)
                self.temp_item.setPen(Qt.NoPen)
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

        elif self.tool == "highlight":
            self.annotations.append({"tipo": "resaltado", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

        self.start_point = None
        super().mouseReleaseEvent(event)

    def deshacer_ultima_anotacion(self):
        if self.graphics_items:
            item = self.graphics_items.pop()
            self.removeItem(item)
        if self.annotations:
            self.annotations.pop()

    def save_image(self, path):
        image = QImage(self.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.render(painter)
        painter.end()
        image.save(path)


class OdontogramaEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Odontograma")

        main_layout = QHBoxLayout()
        tools_layout = QVBoxLayout()
        central_layout = QVBoxLayout()

        # Herramientas
        for name, tool in [("Línea", "line"), ("Círculo", "circle"),
                           ("Pincel", "brush"), ("Resaltado", "highlight")]:
            btn = QPushButton(name)
            btn.clicked.connect(self._make_tool_callback(tool))
            tools_layout.addWidget(btn)

        btn_deshacer = QPushButton("Deshacer")
        btn_deshacer.clicked.connect(self.deshacer_ultima_anotacion)
        tools_layout.addWidget(btn_deshacer)

        btn_guardar = QPushButton("Guardar Imagen")
        btn_guardar.clicked.connect(self.guardar_imagen)
        tools_layout.addWidget(btn_guardar)

        # Fila 1
        fila1 = QHBoxLayout()
        for num in ["18", "17", "16", "15", "14", "13", "12", "11", "21", "22", "23", "24", "25", "26", "27", "28"]:
            campo = QLineEdit(num)
            campo.setAlignment(Qt.AlignCenter)
            campo.setFixedSize(40, 40)
            fila1.addWidget(campo)
        central_layout.addLayout(fila1)

        # Fila 2
        fila2 = QHBoxLayout()
        for num in ["55", "54", "53", "52", "51", "61", "62", "63", "64", "65"]:
            campo = QLineEdit(num)
            campo.setAlignment(Qt.AlignCenter)
            campo.setFixedSize(40, 40)
            fila2.addWidget(campo)
        central_layout.addLayout(fila2)

        # Canvas
        image_path = get_resource_path("ODON.png")
        self.scene = DrawingScene(image_path)
        self.current_scene = self.scene
        view = QGraphicsView(self.scene)
        view.setAlignment(Qt.AlignCenter)
        view.setFixedHeight(300)
        view.setFixedWidth(850)
        central_layout.addWidget(view)

        # Fila 3
        fila3 = QHBoxLayout()
        for num in ["85", "84", "83", "82", "81", "71", "72", "73", "74", "75"]:
            campo = QLineEdit(num)
            campo.setAlignment(Qt.AlignCenter)
            campo.setFixedSize(40, 40)
            fila3.addWidget(campo)
        central_layout.addLayout(fila3)

        # Fila 4
        fila4 = QHBoxLayout()
        for num in ["48", "47", "46", "45", "44", "43", "42", "41", "31", "32", "33", "34", "35", "36", "37", "38"]:
            campo = QLineEdit(num)
            campo.setAlignment(Qt.AlignCenter)
            campo.setFixedSize(40, 40)
            fila4.addWidget(campo)
        central_layout.addLayout(fila4)

        main_layout.addLayout(tools_layout)
        main_layout.addLayout(central_layout)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _make_tool_callback(self, tool_name):
        def set_tool():
            self.current_scene.set_tool(tool_name)
        return set_tool

    def deshacer_ultima_anotacion(self):
        if self.current_scene:
            self.current_scene.deshacer_ultima_anotacion()

    def guardar_imagen(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "PNG (*.png)")
        if file_name:
            self.current_scene.save_image(file_name)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = OdontogramaEditor()
    window.show()
    sys.exit(app.exec())
