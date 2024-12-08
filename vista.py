from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox,QFileDialog, QTextEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QPixmap, QIcon
import os

# Clase para la ventana de inicio de sesión
class VentanaInicio(QMainWindow):
    # Constructor que inicializa la ventana de inicio y carga su interfaz
    def __init__(self, ppal=None):
        super().__init__()
        loadUi('iniciar_sesion.ui', self)  # Carga la interfaz gráfica desde un archivo .ui
        self.setup()  # Configura los elementos gráficos y eventos

    # Configura los elementos de la ventana
    def setup(self):
        self.inicioboton.clicked.connect(self.ValidarUsuario)  # Conecta el botón de inicio al método de validación
        self.contrasenaEdit.setEchoMode(2)  # Configura el campo de contraseña para que oculte los caracteres

        # Conecta el botón del "ojo" para mostrar/ocultar contraseña
        self.ojo.clicked.connect(self.Vercontrasena)
        icon_path = "iconos/ojoabierto.png"
        self.ojo.setIcon(QIcon(icon_path))  # Establece el ícono inicial como "ojo abierto"

        # Configuración de íconos para mejorar la interfaz visual
        self.usuario.setPixmap(QPixmap("iconos/muneco.png"))
        self.contrasena.setPixmap(QPixmap("iconos/contrasena.png"))
        self.iniciarsesion.setPixmap(QPixmap("iconos/sesion.png"))

        # Configuración de ventana
        self.setWindowIcon(QIcon("iconos/iconoventana.png"))  # Ícono de la ventana
        self.setWindowTitle('Iniciar Sesión')  # Título de la ventana

    # Permite agregar un controlador externo para manejar la lógica de negocio
    def addControler(self, c):
        self.__coordinador = c

    # Alterna entre mostrar y ocultar la contraseña
    def Vercontrasena(self):
        if self.contrasenaEdit.echoMode() == 0:  # Si está visible
            self.contrasenaEdit.setEchoMode(2)  # Cambiar a ocultar
            self.ojo.setIcon(QIcon("iconos/ojoabierto.png"))
        elif self.contrasenaEdit.echoMode() == 2:  # Si está oculta
            self.contrasenaEdit.setEchoMode(0)  # Cambiar a visible
            self.ojo.setIcon(QIcon("iconos/ojocerrado.png"))

    # Valida las credenciales del usuario
    def ValidarUsuario(self):
        usuario = self.usuarioEdit.text()  # Obtiene el texto ingresado en el campo de usuario
        contrasena = self.contrasenaEdit.text()  # Obtiene el texto ingresado en el campo de contraseña

        # Llama al coordinador para verificar las credenciales
        if self.__coordinador.Validar(usuario, contrasena):
            ventana_imagenes = VentanaImagenes(self)  # Crea una nueva ventana para imágenes
            ventana_imagenes.addControler(self.__coordinador)  # Asocia el coordinador
            self.hide()  # Oculta la ventana actual
            ventana_imagenes.show()  # Muestra la ventana de imágenes
        else:
            msj = QMessageBox(self)
            msj.setIcon(QMessageBox.Warning)  # Configura el ícono de advertencia
            if self.__coordinador.Validar(usuario, contrasena) is False:
                msj.setText("Contraseña Incorrecta")  # Mensaje de error de contraseña
            else:
                msj.setText("Usuario no existe")  # Mensaje de error de usuario
            msj.show()

# Clase para la ventana de imágenes diagnósticas
class VentanaImagenes(QDialog):
    # Constructor que inicializa la ventana de imágenes
    def __init__(self, ppal):
        super(VentanaImagenes, self).__init__(ppal)
        loadUi('imagenes.ui', self)  # Carga la interfaz gráfica desde un archivo .ui
        self.__parent = ppal  # Guarda referencia a la ventana de inicio
        self.setup()  # Configura los elementos gráficos y eventos

    # Configura los elementos de la ventana de imágenes
    def setup(self):
        # Conecta los eventos de los botones y slider
        self.cargarCarpeta.clicked.connect(self.CargarCarpeta)
        self.horizontalSlider.valueChanged.connect(self.CambiarImagen)
        self.salir.clicked.connect(self.RetornarInicio)
        self.aumentar.clicked.connect(self.incrementSlider)
        self.disminuir.clicked.connect(self.decrementSlider)

        # Configuración de íconos y título de ventana
        self.iconosesion.setPixmap(QPixmap("iconos/iconoventana.png"))
        self.setWindowIcon(QIcon("iconos/iconoventana.png"))
        self.setWindowTitle('Imágenes Diagnósticas')
        self.aumentar.setIcon(QIcon("iconos/aumentar.png"))
        self.disminuir.setIcon(QIcon("iconos/disminuir.png"))

        # Desactivar botones de navegación inicialmente
        self.aumentar.setEnabled(False)
        self.disminuir.setEnabled(False)

    # Incrementa el valor del slider para mostrar la siguiente imagen
    def incrementSlider(self):
        current_value = self.horizontalSlider.value()
        self.horizontalSlider.setValue(current_value + 1)

    # Disminuye el valor del slider para mostrar la imagen anterior
    def decrementSlider(self):
        current_value = self.horizontalSlider.value()
        self.horizontalSlider.setValue(current_value - 1)

    # Permite agregar un controlador externo para manejar la lógica de negocio
    def addControler(self, c):
        self.__coordinador = c

    # Regresa a la ventana de inicio de sesión
    def RetornarInicio(self):
        self.hide()  # Oculta la ventana de imágenes
        self.__parent.show()  # Muestra la ventana de inicio
        self.__parent.usuarioEdit.clear()  # Limpia el campo de usuario
        self.__parent.contrasenaEdit.clear()  # Limpia el campo de contraseña

    # Carga una carpeta de imágenes DICOM
    def CargarCarpeta(self):
        folder_dialog = QFileDialog(self)  # Crea un cuadro de diálogo para seleccionar la carpeta
        folder_dialog.setFileMode(QFileDialog.Directory)  # Solo permite seleccionar carpetas
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if folder_dialog.exec_():
            self.folder_path = folder_dialog.selectedFiles()[0]  # Obtiene la ruta seleccionada
            self.dicom_files = [f for f in os.listdir(self.folder_path) if f.endswith(".dcm")]  # Filtra archivos DICOM
            self.current_index = 0  # Inicializa el índice en 0
            self.load_current_dicom()  # Carga la primera imagen

    # Carga la imagen DICOM actual según el índice
    def load_current_dicom(self):
        if 0 <= self.current_index < len(self.dicom_files):
            file_name = self.dicom_files[self.current_index]  # Obtiene el archivo actual
            file_path = os.path.join(self.folder_path, file_name)  # Construye la ruta completa
            self.__coordinador.img_conextion(file_path)  # Procesa la imagen con el coordinador
            pixmap = QPixmap('temp_image.png')  # Carga la imagen temporal
            self.imagenes.setPixmap(pixmap)  # Muestra la imagen en el QLabel
            os.remove('temp_image.png')  # Elimina el archivo temporal

    # Cambia la imagen mostrada según el valor del slider
    def CambiarImagen(self, value):
        self.current_index = value
        self.load_current_dicom()
