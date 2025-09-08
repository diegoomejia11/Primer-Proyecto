from tarea import Tarea
from archivojson import guardar_Tarea, ls_Tarea

class RepositorioTareas:
    """Gestiona una lista de tareas en memoria con la capacidad de guardar/cargar."""

    def __init__(self):
        self.tareas = []
        self._contador_Tareas = 0

    def add(self, titulo, prioridad, fecha, etiquetas, descripcion):
        """Agrega una nueva tarea al repositorio."""
        self._contador_Tareas += 1
        new_id = f"T-{self._contador_Tareas:04d}"
        tarea = Tarea(new_id, titulo, prioridad, fecha, etiquetas, descripcion)
        self.tareas.append(tarea)
        return tarea

    def ls(self):
        """Lista todas las tareas."""
        return self.tareas

    def find(self, texto):
        """Busca tareas por substring en el título o la descripción."""
        return [  t for t in self.tareas 
            if texto.lower() in t.titulo.lower() or texto.lower() in t.descripcion.lower() ]
  
