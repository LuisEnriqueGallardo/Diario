from PySide6.QtWidgets import QMainWindow, QDialog, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QApplication, QGridLayout, QWidget, QLabel
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QAction, QIcon
from ColoresConsola import Colores
import base64
from PySide6.QtWidgets import QPushButton
from time import sleep

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
        widgetPrincipal = QWidget()
        
        # Crear el menu
        menuSuperior = self.menuBar()
        menuSuperior.setNativeMenuBar(False)
        menuArchivo = menuSuperior.addMenu("Archivo")
        menuEditar = menuSuperior.addMenu("Editar")
        menuVer = menuSuperior.addMenu("Ver")
        menuHerramientas = menuSuperior.addMenu("Herramientas")
                
        # Conectar menus a acciones
        menuArchivo.addAction("Nueva anotación", self.crearAnotacion, "Ctrl+Q")
        
        # Creación de un layout para la ventana principal
        self.layoutPrincipal = QVBoxLayout()
        widgetPrincipal.setLayout(self.layoutPrincipal)
        self.setCentralWidget(widgetPrincipal)
        
        sleep(0.5)
        self.actualizarAnotaciones()
        
    def crearAnotacion(self):
        """Crea una nueva anotación
        """
        nuevaAnotacion = QDialog(self)
        
        layout = QGridLayout()
        nuevaAnotacion.setWindowTitle("Nueva anotación")
        nuevaAnotacion.setModal(True)
        
        textoAnotado = QLineEdit()
        textoAnotado.setPlaceholderText("Titulo")
        
        botonAceptar = QPushButton("Aceptar")
        botonAceptar.clicked.connect(nuevaAnotacion.accept)
        
        botonCancelar = QPushButton("Cancelar")
        botonCancelar.clicked.connect(nuevaAnotacion.reject)
        
        contenidoDeAnotacion = QTextEdit()
        contenidoDeAnotacion.setReadOnly(False)
        
        layout.addWidget(textoAnotado, 0, 0, 1, 2)
        layout.addWidget(botonAceptar, 1, 0)
        layout.addWidget(botonCancelar, 1, 1)
        layout.addWidget(contenidoDeAnotacion, 2, 0, 1, 2)
        
        nuevaAnotacion.setLayout(layout)
        nuevaAnotacion.exec()
        
        if nuevaAnotacion.accepted:
            with open("Anotacion.dat", "a+") as archivo:
                # Se crea un registro con la fecha de creación de la anotación
                registro = f"Anotación creada el {QDate.currentDate().toString(Qt.ISODate)};"
                # Se codifica el texto de la anotación en base64
                texto = f"{registro}__{textoAnotado.text()}//{contenidoDeAnotacion.toPlainText()}"
                # Se escribe el texto codificado en el archivo para tener un registro. Se usa ";" como separador
                archivo.write(f"{base64.b64encode(texto.encode()).decode()};")
                # Se realiza un Log de aviso de éxito
                print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Anotación creada con éxito")
                archivo.close()
                self.actualizarAnotaciones()
                
    def mostrarAnotacion(self, titulo, contenido):
        """Muestra la anotación seleccionada
        """
        # Se realiza un Log de aviso de éxito
        print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Mostrando anotación")
        # Se crea el layout para mostrar la anotación
        layout = QVBoxLayout()
        # Se crea el dialogo para mostrar la anotación
        muestraAnotacion = QDialog(self)
        # Se crea el titulo y el contenido de la anotación
        titulo = QLabel(titulo)
        # Se crea el contenido de la anotación
        contenido = QLabel(contenido)
        # Se crea un botón para cerrar la anotaación
        botonCerrar = QPushButton("Volver")
        botonCerrar.clicked.connect(muestraAnotacion.close)
        
        layout.addWidget(titulo)
        layout.addWidget(contenido)
        layout.addWidget(botonCerrar)
        muestraAnotacion.setWindowTitle(titulo.text())
        muestraAnotacion.setLayout(layout)
        muestraAnotacion.exec()

    def eliminarAnotacion(self, anotacion, contenido):
        """Elimina una anotación
        """
        # Se elimina la anotación de la ventana principal para luego eliminarla del archivo
        anotacion.deleteLater()
        print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Anotación eliminada con éxito")
        try:
            with open("Anotacion.dat", "r") as archivo:
                contenidoNuevo = archivo.read().replace(contenido, "")
                archivo.close()
            with open("Anotacion.dat", "w") as archivo:
                archivo.write(contenidoNuevo)
                archivo.close()
        except:
            pass
        
    def actualizarAnotaciones(self):
        """Actualiza la lista de anotaciones
        """
        try:
            # Se eliminan las anotaciones anteriores limpiando toda la ventana
            while self.layoutPrincipal.count():
                child = self.layoutPrincipal.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                    
            # Se leen las anotaciones del archivo y se reconstruye la ventana completa
            with open("Anotacion.dat", "r") as archivo:
                contenido = archivo.read().split(";")
                print(f"{Colores.AMARILLO}CONSOLA {Colores.RESET}: Anotaciones encontradas: {len(contenido)-1}. {contenido}")
                for anotacion in contenido:
                    # Se recorre el contenido del archivo y se crea un label por cada anotación para mostrarlo
                    if anotacion != "":
                        # Se decodifica el texto de la anotación
                        texto = base64.b64decode(anotacion.encode()).decode()
                        titulo = texto.split("__")[1].split("//")[0]
                        contenido = texto.split("__")[1].split("//")[1]
                        fecha = texto.split("__")[0]
                        
                        # Se crea un label con el texto de la anotación para mostrarlo en la ventana principal
                        labelAnotacion = QPushButton(f"{texto.split('__')[1].split('//')[0]}\n{fecha}")
                        labelAnotacion.clicked.connect(lambda cabecera = titulo, texto = contenido: self.mostrarAnotacion(cabecera, texto))
                        
                        botonBorrar = QPushButton("X", labelAnotacion)
                        botonBorrar.setFlat(True)
                        botonBorrar.clicked.connect(lambda bool="boleano", boton = labelAnotacion, contenido = anotacion: self.eliminarAnotacion(boton, f"{contenido};"))
                        
                        # Se crea un registro con la fecha de creación de la anotación
                        self.layoutPrincipal.addWidget(labelAnotacion)
                archivo.close()
        except:
            pass

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()