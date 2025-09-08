import datetime

class Tarea:
    def __init__(self, numTarea, titulo, prioridad, fecha, etiquetas, descripcion, completada=False):
        if not 1 <= prioridad <= 10:
            raise ValueError("pon nivel de prioridad entre el 1 y 10")
        try:
            datetime.datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            raise ValueError("debes poner: YYYY-MM-DD.")
        self.numTarea = numTarea
        self.titulo = titulo
        self.prioridad = prioridad
        self.fecha = fecha
        self.etiquetas = etiquetas
        self.descripcion = descripcion
        self.completada = completada

    def conver_Diccionario(self):
        """Convierte el objeto Tarea a un diccionario para guardar en JSON."""
        return {
            'id': self.numTarea,
            'titulo': self.titulo,
            'prioridad': self.prioridad,
            'fecha': self.fecha,
            'etiquetas': self.etiquetas,
            'descripcion': self.descripcion,
            'completada': self.completada
        }