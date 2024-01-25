from PySide6.QtWidgets import QMainWindow, QDialog, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QApplication, QGridLayout, QWidget, QLabel
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QIcon, QFont
from ColoresConsola import Colores
import base64
from PySide6.QtWidgets import QPushButton

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
        menuVer = menuSuperior.addMenu("Ver")
        menuHerramientas = menuSuperior.addMenu("Herramientas")
                
        # Conectar menus a acciones
        menuArchivo.addAction("Nueva anotación", self.crearAnotacion, "Ctrl+Q")
        
        # Creación de un layout para la ventana principal
        self.layoutPrincipal = QVBoxLayout()
        widgetPrincipal.setLayout(self.layoutPrincipal)
        self.setCentralWidget(widgetPrincipal)
        self.actualizarAnotaciones()
        self.tituloFuente = QFont("Consolas")
        self.tituloFuente.setPointSize(20)
        self.fuenteContenido = QFont("Consolas")
        self.fuenteContenido.setPointSize(12)
        
    def crearAnotacion(self):
        """Crea una nueva anotación
        """
        nuevaAnotacion = QDialog(self)
        nuevaAnotacion.move(100, 100)
        
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
                registro = f"Anotación creada el {QDate.currentDate().toString(Qt.ISODate)}"
                # Se codifica el texto de la anotación en base64
                texto = f"{registro}__{textoAnotado.text()}//{contenidoDeAnotacion.toPlainText()}"
                # Se escribe el texto codificado en el archivo para tener un registro. Se usa ";" como separador
                archivo.write(f"{base64.b64encode(texto.encode()).decode()};")
                # Se realiza un Log de aviso de éxito
                print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Anotación creada con éxito")
                archivo.close()
                self.actualizarAnotaciones()
                
    def mostrarAnotacion(self, titulo, contenido, anotacion):
        """Muestra la anotación seleccionada
        """
        # Se realiza un Log de aviso de éxito
        print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Mostrando anotación")
        
        # Se crea el layout para mostrar la anotación
        layout = QVBoxLayout()
        
        # Se crea el dialogo para mostrar la anotación
        muestraAnotacion = QDialog(self)
        muestraAnotacion.move(200, 100)
        
        # Se crea el titulo y el contenido de la anotación
        etTitulo = QLabel(titulo)
        etTitulo.setFont(self.tituloFuente)
        
        # Se crea el contenido de la anotación
        etContenido = QLabel(contenido)
        etContenido.setFont(self.fuenteContenido)
        
        # Se crea un botón para cerrar la anotaación
        botonCerrar = QPushButton("Volver")
        botonCerrar.clicked.connect(muestraAnotacion.close)
        
        # Se crea un botón para editar la anotación
        botonEditar = QPushButton("Editar")
        botonEditar.clicked.connect(lambda _='_', contenidoNuevo = anotacion: self.editarAnotacion(contenidoNuevo))
        botonEditar.clicked.connect(muestraAnotacion.close)
        
        layout.addWidget(etTitulo)
        layout.addWidget(etContenido)
        layout.addWidget(botonEditar)
        layout.addWidget(botonCerrar)
        
        muestraAnotacion.setWindowTitle(titulo)
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
                while ";;" in contenidoNuevo:
                    contenidoNuevo = contenidoNuevo.replace(";;", ";")
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
                    if anotacion != '':
                        # Se decodifica el texto de la anotación
                        texto = base64.b64decode(anotacion.encode()).decode()
                        titulo = texto.split("__")[1].split("//")[0]
                        contenidoEscrito = texto.split("__")[1].split("//")[1]
                        fecha = texto.split("__")[0]
                        
                        # Se crea un label con el texto de la anotación para mostrarlo en la ventana principal
                        labelAnotacion = QPushButton(f"{titulo}\n{fecha}")
                        labelAnotacion.clicked.connect(lambda cabecera = titulo, texto = contenidoEscrito, anotacionG = anotacion: self.mostrarAnotacion(cabecera, texto, anotacionG))
                        
                        botonBorrar = QPushButton("X", labelAnotacion)
                        botonBorrar.setFlat(True)
                        botonBorrar.clicked.connect(lambda bool="boleano", boton = labelAnotacion, contenido = anotacion: self.eliminarAnotacion(boton, f"{contenido}"))
                        
                        # Se crea un registro con la fecha de creación de la anotación
                        self.layoutPrincipal.addWidget(labelAnotacion)
                archivo.close()
        except:
            pass

    def editarAnotacion(self, contenido):
        """Función para la edición de las anotaciones
        """
        print(f"{Colores.VERDE}CONSOLA {Colores.RESET}: Editando anotación... {contenido}")
        # Se usa un dialogo para editar la anotación
        ventanaEdicion = QDialog(self)
        ventanaEdicion.setModal(True)
        ventanaEdicion.move(300, 300)
        ventanaEdicion.setWindowTitle("Editar anotación")
        
        layout = QGridLayout()
        
        # Texto original de la anotación
        texto = base64.b64decode(contenido.encode()).decode()
        titulo = texto.split("__")[1].split("//")[0]
        CAnotacion = texto.split("__")[1].split("//")[1]
        fecha = texto.split("__")[0]
        
        # Se crea un campo de texto para el contenido de la anotación
        contenidoDeAnotacion = QTextEdit(CAnotacion)
        contenidoDeAnotacion.setFocus()
        
        # Se crea un botón para aceptar la edición de la anotación
        botonAceptar = QPushButton("Aceptar")
        botonAceptar.clicked.connect(ventanaEdicion.accept)
        
        # Se crea un botón para cancelar la edición de la anotación
        botonCancelar = QPushButton("Cancelar")
        botonCancelar.clicked.connect(ventanaEdicion.reject)
        
        # Se añade todo a un layout para mostrarlo en la ventana
        layout.addWidget(botonAceptar, 0, 0)
        layout.addWidget(botonCancelar, 0, 1)
        layout.addWidget(contenidoDeAnotacion, 1, 0, 1, 2)
        ventanaEdicion.setLayout(layout)
        ventanaEdicion.exec()
        
        # Se realiza la verificación de la edición de la anotación para guardarla y reemplazarla por la anterior
        if ventanaEdicion.accept:
            try:
                with open("Anotacion.dat", "r") as archivo:
                    formatoOriginal = f"{fecha}__{titulo}//{contenidoDeAnotacion.toPlainText()}"
                    anotacionCompletaNueva = base64.b64encode(formatoOriginal.encode()).decode()
                    contenidoNuevo = archivo.read().replace(contenido, anotacionCompletaNueva)
                    archivo.close()
                with open("Anotacion.dat", "w") as archivo:
                    archivo.write(contenidoNuevo)
                    archivo.close()
                self.actualizarAnotaciones()
                self.mostrarAnotacion(titulo, contenidoDeAnotacion.toPlainText())
            except:
                pass        
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()