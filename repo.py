from tarea import Tarea
"""Importa la clase Tarea que representa cada tarea individual"""

from archivojson import guardar_Tarea, cargar_tareas_json
"""Importa funciones para guardar y cargar listas de tareas en archivos JSON"""


class RepositorioTareas:
    """
    Gestiona una lista de tareas en memoria con capacidad de guardarlas y cargarlas desde archivo
    """

    def __init__(self):
        """
        Inicializa el repositorio con lista vacia y contador interno para IDs
        """
        self.tareas = []
        self._contador_Tareas = 0

    def add(self, titulo, prioridad, fecha, etiquetas, descripcion):
        """
        Agrega una tarea nueva con un ID autogenerado incrementando el contador
        Crea la tarea con todos los campos y la añade a la lista interna
        Devuelve la tarea creada
        """
        self._contador_Tareas += 1
        new_id = f"T-{self._contador_Tareas:04d}"
        tarea = Tarea(new_id, titulo, prioridad, fecha, etiquetas, descripcion)
        self.tareas.append(tarea)
        return tarea

    def ls(self):
        """
        Devuelve la lista de todas las tareas guardadas en memoria
        """
        return self.tareas

    def find(self, texto):
        """
        Busca texto en minusculas dentro del titulo o descripcion de las tareas
        Devuelve las tareas que coincidan
        """
        return [t for t in self.tareas if texto.lower() in t.titulo.lower() or texto.lower() in t.descripcion.lower()]

    def rm(self, numTarea):
        """
        Elimina la tarea que tenga el ID igual a numTarea
        Retorna True si se elimino alguna tarea, False si no se encontro
        """
        contador_inicial = len(self.tareas)
        self.tareas = [t for t in self.tareas if t.id != numTarea]
        return len(self.tareas) < contador_inicial

    def done(self, numTarea):
        """
        Marca como completada la tarea que coincida con el ID dado
        Devuelve True si la tarea fue encontrada y marcada, False si no se encontro
        """
        for t in self.tareas:
            if t.id == numTarea:
                t.completada = True
                return True
        return False

    def save(self, archivo_ruta):
        """
        Guarda la lista actual de tareas en un archivo JSON usando guardar_Tarea
        Devuelve True si fue exitoso, False si hubo error
        """
        return guardar_Tarea(archivo_ruta, self.tareas)

    def load(self, archivo_ruta):
        """
        Carga las tareas desde un archivo JSON usando cargar_tareas_json
        Reemplaza la lista interna de tareas y actualiza el contador de IDs
        Devuelve True si la carga fue exitosa, False si el archivo esta vacio o no existe
        """
        tareas_diccionarios = cargar_tareas_json(archivo_ruta)
        if not tareas_diccionarios:
            self.tareas = []
            self._contador_Tareas = 0
            return False  

        tareas_cargadas = []
        max_id = 0
        for d in tareas_diccionarios:
            tarea = Tarea(**d)
            tareas_cargadas.append(tarea)
            if tarea.id.startswith('T-'):
                try:
                    num_id = int(tarea.id.split('T-')[1])
                    if num_id > max_id:
                        max_id = num_id
                except (ValueError, IndexError):
                    pass

        self.tareas = tareas_cargadas
        self._contador_Tareas = max_id
        return True
