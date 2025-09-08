import argparse
from repo import RepositorioTareas

def main():
    repo = RepositorioTareas()
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    # subparser para add
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--titulo', required=True)
    add_parser.add_argument('--prioridad', type=int, required=True)
    add_parser.add_argument('--fecha', required=True)
    add_parser.add_argument('--etiquetas')
    add_parser.add_argument('--descripcion')

    # subparser para ls
    ls_parser = subparsers.add_parser('ls')
    ls_parser.add_argument('--por', choices=['fecha', 'prioridad', 'titulo'])

    # subparser para find
    find_parser = subparsers.add_parser('find')
    find_parser.add_argument('texto')
   
   # subparser pasa save
    save_parser = subparsers.add_parser('save', help='Guarda las tareas en un archivo JSON.')
    save_parser.add_argument('file_path', help='Ruta del archivo para guardar las tareas.')

     # subparser para load
    load_parser = subparsers.add_parser('load', help='Carga tareas desde un archivo JSON.')
    load_parser.add_argument('file_path', help='Ruta del archivo para cargar las tareas.')
    

    args = parser.parse_args()

    if args.command == 'add':
        etiquetas = [e.strip() for e in args.etiquetas.split(',') if e.strip()]
        try:
            tarea = repo.add(args.titulo, args.prioridad, args.fecha, etiquetas, args.descripcion)
            print(f"Tarea {tarea.numTarea} agregada con éxito.")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == 'ls':
        tareas = repo.ls()
        if args.por:
            if args.por == 'fecha':
                tareas.sort(key=lambda t: t.fecha)
            elif args.por == 'prioridad':
                tareas.sort(key=lambda t: t.prioridad)
            elif args.por == 'titulo':
                tareas.sort(key=lambda t: t.titulo)

        if not tareas:
            print("No hay tareas en la agenda.")
        else:
            for t in tareas:
                status = "[Completada]" if t.completada else "[Pendiente]"
                print(f"ID: {t.numTarea} {status} Título: {t.titulo}, Prioridad: {t.prioridad}, Fecha: {t.fecha}")

    elif args.command == 'find':
        found_tasks = repo.find(args.texto)
        if not found_tasks:
            print(f"No se encontraron tareas con '{args.texto}'.")
        else:
            for t in found_tasks:
                print(f"ID: {t.numTarea}, Título: {t.titulo}, Prioridad: {t.prioridad}")
    
if __name__ == "__main__":
    main()