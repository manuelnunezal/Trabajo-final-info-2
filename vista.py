from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox,QFileDialog, QTextEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QPixmap, QIcon
import os

class VentanaInicio(QMainWindow):
    def __init__(self, ppal =None):
        super().__init__()
        loadUi('iniciar_sesion.ui',self)
        self.setup()

    def setup(self):
        self.inicioboton.clicked.connect(self.ValidarUsuario)
        self.contrasenaEdit.setEchoMode(2)
        self.ojo.clicked.connect(self.Vercontrasena)
        icon_path = "iconos/ojoabierto.png"  
        icon = QIcon(icon_path)
        self.ojo.setIcon(icon)    
        icon_usua = "iconos/muneco.png"
        pixmapusua = QPixmap(icon_usua)
        self.usuario.setPixmap(pixmapusua)
        icon_contra = "iconos/contrasena.png"
        pixmapcontra = QPixmap(icon_contra)
        self.contrasena.setPixmap(pixmapcontra)
        icon_iniciarse = "iconos/sesion.png"
        pixmapiniciarse = QPixmap(icon_iniciarse)
        self.iniciarsesion.setPixmap(pixmapiniciarse)
        icon_window = QIcon("iconos/iconoventana.png")
        self.setWindowIcon(icon_window)
        self.setWindowTitle('Iniciar Sesión')

    def addControler(self, c):
        self.__coordinador = c

    def Vercontrasena(self):
        if self.contrasenaEdit.echoMode() == 0:
            self.contrasenaEdit.setEchoMode(2)
            icon_path = "iconos/ojoabierto.png"  
            icon = QIcon(icon_path)
            self.ojo.setIcon(icon)
        elif self.contrasenaEdit.echoMode() == 2:
            self.contrasenaEdit.setEchoMode(0)
            icon_path = "iconos/ojocerrado.png"  
            icon = QIcon(icon_path)
            self.ojo.setIcon(icon)
        

    def ValidarUsuario(self):
        usuario = self.usuarioEdit.text()
        contrasena = self.contrasenaEdit.text()
        
        if self.__coordinador.Validar(usuario, contrasena) == True:
            ventana_imagenes=VentanaImagenes(self)
            ventana_imagenes.addControler(self.__coordinador)
            self.hide()
            ventana_imagenes.show()
            
            
        elif self.__coordinador.Validar(usuario, contrasena) == False:
            msj= QMessageBox(self)
            msj.setIcon(QMessageBox.Warning) 
            msj.setText("Contraseña Incorrecta")
            msj.show()

        else:
            msj= QMessageBox(self)
            msj.setIcon(QMessageBox.Warning) 
            msj.setText("Usuario no existe")
            msj.show()


class VentanaImagenes(QDialog):
    def __init__(self, ppal):
        super(VentanaImagenes, self).__init__(ppal)
        loadUi('imagenes.ui',self)
        self.__parent=ppal
        self.setup()
           
    def setup(self):
        self.cargarCarpeta.clicked.connect(self.CargarCarpeta)
        self.horizontalSlider.valueChanged.connect(self.CambiarImagen)
        self.salir.clicked.connect(self.RetornarInicio)
        icon_path1 = "iconos/iconoventana.png"
        pixmap1 = QPixmap(icon_path1)
        self.iconosesion.setPixmap(pixmap1)
        icon_window = QIcon("iconos/iconoventana.png")
        self.setWindowIcon(icon_window)
        self.setWindowTitle('Imágenes Diagnósticas')
        self.aumentar.clicked.connect(self.incrementSlider)
        self.disminuir.clicked.connect(self.decrementSlider)
        icon_aumentar = QIcon("iconos/aumentar.png")
        self.aumentar.setIcon(icon_aumentar)
        icon_disminuir = QIcon("iconos/disminuir.png")
        self.disminuir.setIcon(icon_disminuir)
        self.aumentar.setEnabled(False)
        self.disminuir.setEnabled(False)
    
    def incrementSlider(self):
        current_value = self.horizontalSlider.value()
        self.horizontalSlider.setValue(current_value + 1)

    def decrementSlider(self):
        current_value = self.horizontalSlider.value()
        self.horizontalSlider.setValue(current_value - 1)
        
            
    def addControler(self,c):
        self.__coordinador=c
        
    def RetornarInicio(self):
        self.hide()
        self.__parent.show()
        self.__parent.usuarioEdit.clear()
        self.__parent.contrasenaEdit.clear()
        
    def CargarCarpeta(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if folder_dialog.exec_():
            self.folder_path = folder_dialog.selectedFiles()[0]
            self.dicom_files = [f for f in os.listdir(self.folder_path) if f.endswith(".dcm")]
            self.current_index = 0
            self.load_current_dicom()    
        file_name = self.dicom_files[self.current_index]
        file_path = os.path.join(self.folder_path, file_name)
        self.__coordinador.img_conextion(file_path)
        pixmap = QPixmap('temp_image.png')
        self.imagenes.setPixmap(pixmap)
        os.remove('temp_image.png')
        info = self.__coordinador.read_dicom_metadata(file_path)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(info)
        self.info.setWidget(self.text_edit)

        if file_path != '':
            self.aumentar.setEnabled(True)
            self.disminuir.setEnabled(True)
       


    
