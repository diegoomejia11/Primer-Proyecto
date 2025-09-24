import os
import pytest
from tarea import Tarea
from repo import RepositorioTareas
from archivojson import guardar_Tarea, cargar_tareas_json

@pytest.fixture
def repo():
    return RepositorioTareas()

def test_agegrar_comprobar_tamanno(repo):
    # Agregar dos tareas y verificar que ls tiene tamaño 2
    t1 = repo.add("Tarea1", 2, "2025-09-12", ["escuela"], "descripcion 1")
    t2 = repo.add("Tarea2", 3, "2025-09-19", ["trabajo"], "descripcion 2")
    tareas = repo.ls()
    assert len(tareas) == 2
    assert tareas[0].titulo == "Tarea1"
    assert tareas[1].titulo == "Tarea2"

def test_buscar(repo):
    # Agregar tarea, buscar texto debe devolver la tarea
    repo.add("terminar proyecto", 5, "2025-09-23", ["escuela", "tarea"], "proyecto en python")
    resultados = repo.find("proyecto")
    assert len(resultados) == 1
    assert resultados[0].titulo == "terminar proyecto"

def test_guardar_cargar(tmp_path):
    repo = RepositorioTareas()
    repo.add("Prueba guardar", 1, "2025-09-12", ["prueba"], "guardar y cargar")
    ruta = tmp_path / "agenda_test.json"
    # Guardar tareas
    exito = repo.save(str(ruta))
    assert exito
    assert ruta.exists()

    # Crear nuevo repo y cargar
    repo2 = RepositorioTareas()
    cargado = repo2.load(str(ruta))
    assert cargado
    tareas = repo2.ls()
    assert len(tareas) == 1
    assert tareas[0].titulo == "Prueba guardar"
    assert tareas[0].prioridad == 1

def completar_tarea(repo):
    tarea = repo.add("Completar la tarea", 4, "2025-09-10", [], "marcar completada")
    id = tarea.id
    # Marcar completada
    exito_done = repo.done(id)
    assert exito_done
    assert repo.ls()[0].completada is True

def completar_tarea(repo):
    # Eliminar tarea
    tarea = repo.add("Completar la tarea", 4, "2025-09-10", [], "eliminar tarea")
    id_tarea = tarea.id
    exito_rm = repo.rm(id)
    assert exito_rm
    assert len(repo.ls()) == 0

def test_tarea_fecha_prioridad():
    # Fecha inválida debe lanzar ValueError
    with pytest.raises(ValueError):
        Tarea("T-0001", "Titulo", 1, "2025-13-01", [], "")

    # Prioridad inválida
    with pytest.raises(ValueError):
        Tarea("T-0002", "Titulo", 7, "2025-12-01", [], "")

def test_archivojson_guardar_y_cargar(tmp_path):
    tareas = [
        Tarea("T-0001", "prueba1", 1, "2025-09-12", ["test"], "desc1"),
        Tarea("T-0002", "prueba2", 2, "2025-09-22", [], "desc2"),
    ]
    ruta = tmp_path / "test.json"
    exito_guardar = guardar_Tarea(str(ruta), tareas)
    assert exito_guardar
    datos = cargar_tareas_json(str(ruta))
    assert isinstance(datos, list)
    assert len(datos) == 2
    assert datos[0]['titulo'] == "prueba1"
    assert datos[1]['prioridad'] == 2
