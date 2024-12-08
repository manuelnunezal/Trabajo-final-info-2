from PyQt5.QtWidgets import QApplication
from modelo import Usuario
from vista import VentanaInicio
import sys

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def img_conextion(self, carpeta):
        self.modelo.picture_creator(carpeta)
    
    def Validar(self, usuario, contrasena):
        return self.modelo.Validar(usuario, contrasena)
    
    def read_dicom_metadata(self, file_path):
        return self.modelo.read_dicom_metadata(file_path)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    modelo = Usuario()
    vista = VentanaInicio()
    mi_controlador=Controlador(modelo,vista)
    vista.addControler(mi_controlador)
    vista.show()
    sys.exit(app.exec_())