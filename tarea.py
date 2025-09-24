import datetime
"""Modulo para manejo y validacion de fechas"""


class Tarea:
    """
    Representa una tarea con id, titulo, prioridad, fecha, etiquetas,
    descripcion y estado de completada o no
    """

    def __init__(self, id, titulo, prioridad, fecha, etiquetas, descripcion, completada=False):
        """
        Inicializa la tarea verificando que prioridad este entre 1 y 5
        Valida que la fecha tenga formato YYYY-MM-DD, si no lanza ValueError
        Asigna todos los atributos recibidos, incluyendo completada (default False)
        """
        if not 1 <= prioridad <= 5:
            raise ValueError("La prioridad debe estar entre 1 y 5.")
        try:
            datetime.datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            raise ValueError("la fecha debe ser YYYY-MM-DD.")
        self.id = id
        self.titulo = titulo
        self.prioridad = prioridad
        self.fecha = fecha
        self.etiquetas = etiquetas
        self.descripcion = descripcion
        self.completada = completada

    def convertir_aDiccionario(self):
        """
        Convierte la tarea a un diccionario con sus atributos,
        para facilitar su serializacion a JSON o manipulacion
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'prioridad': self.prioridad,
            'fecha': self.fecha,
            'etiquetas': self.etiquetas,
            'descripcion': self.descripcion,
            'completada': self.completada
        }
