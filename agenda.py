import argparse
"""Importamos argpase para poder manejar y introducir datos por la consola"""

from repo import RepositorioTareas
"""Clase para ver todas las tareas que se han hecho"""

from archivojson import cargar_tareas_json
"""cargar tareas desde archivos JSON"""


def main():
    """
    Funcion principal que ejecuta la aplicacion de consola para gestionar tareas
    Carga las tareas desde un archivo, interpreta comandos y argumentos
    Permite agregar, listar, buscar, marcar completadas, eliminar, guardar, cargar y ver tareas
    """

    repo = RepositorioTareas()
    """Crea una instancia del repositorio para manipular las tareas"""

    archivo_guardado = "tareas.json"
    """Archivo JSON donde se guardan o cargan las tareas"""

    repo.load(archivo_guardado)
    """Carga las tareas desde el archivo para tenerlas disponibles en memoria"""

    parser = argparse.ArgumentParser()
    """Inicializa el parser para interpretar argumentos pasados por consola"""

    subparsers = parser.add_subparsers(dest='command', required=True)
    """
    Define los subcomandos disponibles que el programa puede recibir,
    por ejemplo: add, ls, find, done, rm, save, load, view
    """

    add_parser = subparsers.add_parser('add')
    """Subcomando 'add' para agregar una tarea"""

    add_parser.add_argument('--titulo', required=True)
    """Argumento obligatorio para el titulo de la tarea"""

    add_parser.add_argument('--prioridad', type=int, required=True)
    """Argumento obligatorio entero para la prioridad"""

    add_parser.add_argument('--fecha', required=True)
    """Argumento obligatorio con la fecha de la tarea"""

    add_parser.add_argument('--etiquetas')
    """Argumento opcional con etiquetas separadas por comas"""

    add_parser.add_argument('--descripcion')
    """Argumento opcional para la descripcion de la tarea"""

    ls_parser = subparsers.add_parser('ls')
    """Subcomando 'ls' para listar tareas"""

    ls_parser.add_argument('--por', choices=['fecha', 'prioridad', 'titulo'])
    """Argumento opcional para ordenar la lista por fecha, prioridad o titulo"""

    find_parser = subparsers.add_parser('find')
    """Subcomando 'find' para buscar tareas que contengan un texto"""

    find_parser.add_argument('texto')
    """Argumento obligatorio con el texto a buscar"""

    done_parser = subparsers.add_parser('done')
    """Subcomando 'done' para marcar una tarea como completada"""

    done_parser.add_argument('id')
    """Argumento obligatorio con el id de la tarea a marcar"""

    rm_parser = subparsers.add_parser('rm')
    """Subcomando 'rm' para eliminar una tarea"""

    rm_parser.add_argument('id')
    """Argumento obligatorio con el id de la tarea a eliminar"""

    save_parser = subparsers.add_parser('save')
    """Subcomando 'save' para guardar la agenda en un archivo"""

    save_parser.add_argument('file_path')
    """Argumento obligatorio con la ruta del archivo donde guardar"""

    load_parser = subparsers.add_parser('load')
    """Subcomando 'load' para cargar una agenda desde archivo"""

    load_parser.add_argument('file_path')
    """Argumento obligatorio con la ruta del archivo a cargar"""

    view_parser = subparsers.add_parser('view')
    """Subcomando 'view' para mostrar el contenido de un archivo de tareas"""

    view_parser.add_argument('file_path')
    """Argumento obligatorio con la ruta del archivo a mostrar"""

    args = parser.parse_args()
    """Procesa y extrae los argumentos recibidos desde consola"""

    if args.command == 'add':
        """
        Si el comando es 'add', agrega una nueva tarea con los datos recibidos
        Convierte etiquetas en lista, agrega tarea, muestra mensaje y guarda
        """
        etiquetas = [e.strip() for e in args.etiquetas.split(',')] if args.etiquetas else []
        try:
            tarea = repo.add(args.titulo, args.prioridad, args.fecha, etiquetas, args.descripcion)
            print(f"Tarea {tarea.id} se agrego correctamente :3")
            repo.save(archivo_guardado)
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == 'ls':
        """
        Si el comando es 'ls', lista las tareas
        Opcionalmente ordena segun parametro recibido
        """
        tareas = repo.ls()
        if args.por:
            tareas.sort(key=lambda t: getattr(t, args.por))
        if not tareas:
            print("No hay tareas en la agenda.")
        else:
            for t in tareas:
                status = "[Completada]" if t.completada else "[Pendiente]"
                print(f"\nID: {t.id} {status}\nTítulo: {t.titulo}\nPrioridad: {t.prioridad}\nFecha: {t.fecha}\nEtiquetas: {', '.join(t.etiquetas)}\nDescripción: {t.descripcion}\n")

    elif args.command == 'find':
        """
        Si el comando es 'find', busca y muestra tareas que contengan el texto dado
        """
        found_tasks = repo.find(args.texto)
        if not found_tasks:
            print(f"No se encontraron tareas con '{args.texto}'.")
        else:
            for t in found_tasks:
                print(f"ID: {t.id}, Título: {t.titulo}, Prioridad: {t.prioridad}")

    elif args.command == 'done':
        """
        Si el comando es 'done', marca la tarea con el id dado como completada y guarda
        """
        if repo.done(args.id):
            print(f"Tarea {args.id} marcada como completada.")
            repo.save(archivo_guardado)
        else:
            print(f"No se encontró la tarea con ID {args.id}.")

    elif args.command == 'rm':
        """
        Si el comando es 'rm', elimina la tarea indicada por id y guarda los cambios
        """
        if repo.rm(args.id):
            print(f"Tarea {args.id} se elimino la correctamente")
            repo.save(archivo_guardado)
        else:
            print(f"No se encontró la tarea con ID {args.id}.")

    elif args.command == 'save':
        """
        Si el comando es 'save', guarda la agenda en el archivo especificado
        Añade extension '.json' si no existe
        """
        file_path = args.file_path
        if not file_path.endswith('.json'):
            file_path += '.json'
        if repo.save(file_path):
            print(f"Agenda guardada en {file_path}.")
        else:
            print(f"Error, No se pudo guardar el archivo")

    elif args.command == 'load':
        """
        Si el comando es 'load', carga la agenda desde el archivo especificado
        """
        if repo.load(args.file_path):
            print(f"Agenda cargada desde {args.file_path}.")
        else:
            print(f"Error, No se pudo cargar el archivo")

    elif args.command == 'view':
        """
        Si el comando es 'view', muestra en consola el contenido de un archivo JSON de tareas
        """
        try:
            tareas_data = cargar_tareas_json(args.file_path)
            if not tareas_data:
                print(f"El archivo {args.file_path} esta vacío o no hay ninguna tarea")
            else:
                for tarea_dict in tareas_data:
                    print(f"\nID: {tarea_dict.get('id')}\nTítulo: {tarea_dict.get('titulo')}\nPrioridad: {tarea_dict.get('prioridad')}\nFecha: {tarea_dict.get('fecha')}\nEtiquetas: {', '.join(tarea_dict.get('etiquetas', []))}\nDescripción: {tarea_dict.get('descripcion')}\nCompletada: {tarea_dict.get('completada')}\n")
        except FileNotFoundError:
            print(f"Error: El archivo {args.file_path} no se encontro :()")


if __name__ == "__main__":
    """
     solo ejecuta main() si es el archivo principal
    """
    main()
