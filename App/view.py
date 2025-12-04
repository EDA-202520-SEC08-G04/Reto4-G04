import sys
from App import logic as lg
from tabulate import tabulate # type: ignore
from DataStructures.Graph import digraph as G
from DataStructures.List import array_list as lt


def new_logic():
    """
    Se crea una instancia del controlador
    """
    return lg.new_logic()


def print_menu():
    print("\n" + "=" * 40)
    print("       SISTEMA DE MIGRACIÓN DE AVES")
    print("=" * 40)
    print("0. Cargar información")
    print("1. Ejecutar Requerimiento 1")
    print("2. Ejecutar Requerimiento 2")
    print("3. Ejecutar Requerimiento 3")
    print("4. Ejecutar Requerimiento 4")
    print("5. Ejecutar Requerimiento 5")
    print("6. Ejecutar Requerimiento 6")
    print("7. Salir")
    print("=" * 40)


# ----------------------- helpers de impresión ----------------------- #

def _tags_to_python_list(info):
    """
    Convierte info['tags'] (array_list) a lista normal de Python.
    Si no hay 'tags', intenta usar 'tag_id'.
    """
    tags = info.get("tags", None)

    # Caso normal: tags es un array_list {'elements': [...], 'size': n}
    if tags is not None and "elements" in tags and "size" in tags:
        res = []
        n = lt.size(tags)
        for i in range(n):
            res.append(lt.get_element(tags, i))
        return res

    # Si no hay lista de tags pero sí un tag_id suelto
    tag_id = info.get("tag_id", None)
    if tag_id is not None:
        return [tag_id]

    # Si no hay información de grullas
    return ["N/A"]


def _cmp_vertex_fecha(v1, v2):
    """
    Criterio para ordenar vértices por fecha de creación ascendente.
    """
    return v1["creation_time"] < v2["creation_time"]


# ----------------------- vista: carga de datos ----------------------- #

def load_data(control):
    """
    Carga los datos y muestra el reporte (estadísticas + primeros/últimos 5 nodos)
    """
    filename = input("Ingrese el nombre del archivo (Enter para default large): ")
    if not filename:
        filename = "1000_cranes_mongolia_large.csv"

    # Llamada a la lógica
    lg.load_data(control, filename)

    # --- 1. ESTADÍSTICAS GENERALES ---
    grafo = control["grafo_distancia"]
    n_nodos = G.order(grafo)
    n_arcos = G.size(grafo)

    n_events = control.get("total_eventos", 0)
    if n_events == 0:
        n_events = lt.size(control["lista_eventos"])

    stats = [
        ["Total de grullas reconocidas:", control.get("total_grullas", 0)],
        ["Total de eventos cargados:", n_events],
        ["Total de nodos del grafo:", n_nodos],
        ["Total de arcos en el grafo:", n_arcos]
    ]

    print("\n" + "=" * 40)
    print("CARGA DE DATOS")
    print("=" * 40)
    print(tabulate(stats, tablefmt="plain"))
    print("=" * 40 + "\n")

    print("DETALLE DE NODOS (VÉRTICES)")
    print("=" * 40)

    # --- 2. OBTENER Y ORDENAR VÉRTICES POR FECHA ---
    vertices_keys = G.vertices(grafo)
    total_vertices = lt.size(vertices_keys)

    # Construimos una lista con la información de cada vértice
    lista_vertices_info = lt.new_list()
    for i in range(total_vertices):
        key = lt.get_element(vertices_keys, i)
        info = G.get_vertex_information(grafo, key)
        lt.add_last(lista_vertices_info, info)

    # Ordenar por creation_time ascendente
    lt.quick_sort(lista_vertices_info, _cmp_vertex_fecha)

    headers = [
        "Identificador único",
        "Posición (lat, lon)",
        "Fecha de creación",
        "Grullas (tags)",
        "Conteo de eventos"
    ]

    # --- 3. TABLA PRIMEROS 5 NODOS ---
    print("\n--- Primeros 5 Nodos ---")
    table_data_first = []
    limite_first = 5 if total_vertices > 5 else total_vertices

    for i in range(limite_first):
        info = lt.get_element(lista_vertices_info, i)
        pos_str = f"({info['lat']:.5f}, {info['lon']:.5f})"
        fecha_str = str(info["creation_time"])
        tags_py = _tags_to_python_list(info)

        table_data_first.append([
            info["id"],
            pos_str,
            fecha_str,
            tags_py,
            info["event_count"]
        ])

    print(tabulate(table_data_first, headers=headers, tablefmt="grid"))

    # --- 4. TABLA ÚLTIMOS 5 NODOS ---
    if total_vertices > 5:
        print("\n--- Últimos 5 Nodos ---")
        table_data_last = []
        start_index = total_vertices - 5

        for i in range(start_index, total_vertices):
            info = lt.get_element(lista_vertices_info, i)
            pos_str = f"({info['lat']:.5f}, {info['lon']:.5f})"
            fecha_str = str(info["creation_time"])
            tags_py = _tags_to_python_list(info)

            table_data_last.append([
                info["id"],
                pos_str,
                fecha_str,
                tags_py,
                info["event_count"]
            ])

        print(tabulate(table_data_last, headers=headers, tablefmt="grid"))

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def _convert_nodos_tabla(lista_nodos):
    """
    Convierte la lista de nodos del modelo al formato lista de listas
    para que tabulate pueda imprimirla correctamente.
    """
    tabla = []
    for nodo in lista_nodos:
        row = [
            nodo["id"],
            nodo["lat"],
            nodo["lon"],
            nodo["num_grullas"],
            ", ".join(nodo["tags_preview"]) if nodo["tags_preview"] else "Unknown",
            f"{nodo['dist_next']:.2f}"
        ]
        tabla.append(row)
    return tabla

def print_req_1(control):
    """
    Imprime el resultado del Requerimiento 1 usando tabulate.
    El parámetro 'resultado' es el diccionario retornado por el modelo.
    """
    lat_or=float(input("introduzca la latitud de origen: "))
    lon_or=float(input("introduzca la longitud de origen: "))
    lat_dest=float(input("introduzca la latitud de destino: "))
    lon_dest=float(input("introduzca la longitud de destino: "))
    grulla_id=input("introduzca ID del individuo: ")
    resultado=lg.req_1(control,lat_or, lon_or, lat_dest, lon_dest, grulla_id)
    
    if "error" in resultado:
        print("\n  No se pudo encontrar un camino válido:")
        print("   →", resultado["error"])
        return

    print("\n====== REQUERIMIENTO 1: Camino migratorio del individuo ======\n")

    print(f"Primer nodo donde se detectó al individuo:")
    print(f" → Nodo: {resultado['nodo_inicio_grulla']}\n")

    print(f"Distancia total del camino: {resultado['distancia_total']:.2f} km")
    print(f"Total de puntos en la ruta: {resultado['total_puntos']}\n")

    print("===== Primeros 5 puntos de la ruta =====")
    print(tabulate(_convert_nodos_tabla(resultado["primeros_5"]),
                   headers=["Nodo", "Latitud", "Longitud", "#Grullas", "Tags (3 primeros / 3 últimos)", "Distancia al siguiente (km)"],
                   tablefmt="grid"))

    print("\n===== Últimos 5 puntos de la ruta =====")
    print(tabulate(_convert_nodos_tabla(resultado["ultimos_5"]),
                   headers=["Nodo", "Latitud", "Longitud", "#Grullas", "Tags (3 primeros / 3 últimos)", "Distancia al siguiente (km)"],
                   tablefmt="grid"))

    print("\n===============================================================\n")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
