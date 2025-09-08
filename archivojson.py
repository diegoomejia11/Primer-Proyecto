import json

def guardar_Tarea(file_path, tareas):
    """Guarda una lista de objetos Tarea en un archivo JSON."""
    try:
        conv_diccionario = [t.convertir_aDiccionario() for t in tareas]
        with open(file_path, 'w', encoding='utf-8') as f:
          json.dump(conv_diccionario, f, indent=4)
          return True
    except (IOError, TypeError):
       return False

def ls_Tarea(file_path):
    """Carga tareas desde un archivo JSON y las devuelve como una lista de diccionarios."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
         return json.load(f)
    except (IOError, json.JSONDecodeError):
        return []