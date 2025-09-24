import json
"""Modulo para trabajar con archivos JSON (leer y escribir)"""


def guardar_Tarea(file_path, tareas):
    """
    Guarda la lista de tareas en un archivo JSON indicado por file_path
    Convierte cada tarea a diccionario usando convertir_aDiccionario()
    Escribe el JSON 
    Devuelve True si se guardo exitosamente, False si hubo error de IO o tipo
    """
    try:
        conv_diccionario = [t.convertir_aDiccionario() for t in tareas]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(conv_diccionario, f, indent=4)
        return True
    except (IOError, TypeError):
        return False


def cargar_tareas_json(file_path):
    """
    Carga y devuelve la lista de tareas desde el archivo JSON indicado
    Devuelve lista vacia si hubo error al abrir o parsear el archivo
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return []
