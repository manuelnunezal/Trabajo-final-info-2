from PyQt5.QtCore import QObject
import pydicom
import matplotlib.pyplot as plt

class Usuario(QObject):
    def __init__(self):
        self.__usuario="medicoAnalitico" 
        self.__contrasena="bio12345"
        self.__usuarios = {self.__usuario:self.__contrasena} 

    def Validar(self, usuario, contrasena):
        if usuario in self.__usuarios.keys():
            if contrasena == self.__usuarios[usuario]:
                return True
            else:
                return False
        else:
            return None

    def picture_creator(self, carpeta):
        ds = pydicom.dcmread(carpeta)
        pixel_data = ds.pixel_array
        if (len(pixel_data.shape))==3:
            slice_index = pixel_data.shape[0] // 2
            selected_slice = pixel_data[slice_index, :, :]
            plt.imshow(selected_slice, cmap=plt.cm.bone)
        else:
            plt.imshow(pixel_data, cmap = plt.cm.bone)
        plt.axis('off')
        plt.savefig("temp_image.png")
        
    def read_dicom_metadata(self, file_path):
        ds = pydicom.dcmread(file_path)      
        info_imagen = 'Información DICOM: ' + '\n'
        nombre = f'Nombre del paciente: {ds['PatientName'].value}' 
        modalidad = f'Modalidad del estudio: {ds['Modality'].value}'
        descripcion= f'Descripción del estudio: {ds['StudyDescription'].value}'
        acquisition_date = ds['AcquisitionDate']
        formatted_date = f'{acquisition_date[:4]}-{acquisition_date[4:6]}-{acquisition_date[6:8]}'
        fecha =f'Fecha: {formatted_date}'
        serie = f'Descripción de la serie: {ds['SeriesDescription'].value}'
        info_imagen= info_imagen + '\n' + nombre + '\n' + modalidad + '\n'+ descripcion + '\n' + fecha + '\n' + serie
        return info_imagen

     
          