from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    """Ventana principal para el diario personal

    Args:
        QMainWindow (QMainWindow): Ventana principal
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diario Personal v1.0")
        self.setMinimumSize(480, 320)
        self.setWindowIcon(QIcon("IconoPrincipal.png"))
        
        # Crear el menu
        menuSuperior = self.menuBar()
        menuSuperior.setNativeMenuBar(False)
        menuArchivo = menuSuperior.addMenu("Archivo")
        menuEditar = menuSuperior.addMenu("Editar")
        menuVer = menuSuperior.addMenu("Ver")
        menuHerramientas = menuSuperior.addMenu("Herramientas")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()