import sys
from App import logic as lg
from tabulate import tabulate
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



def _tags_to_python_list(info):
    """
    Convierte info['tags'] (array_list) a lista normal de Python.
    Si no hay 'tags', intenta usar 'tag_id'.
    """
    tags = info.get("tags", None)

    if tags is not None and "elements" in tags and "size" in tags:
        res = []
        n = lt.size(tags)
        for i in range(n):
            res.append(lt.get_element(tags, i))
        return res

    tag_id = info.get("tag_id", None)
    if tag_id is not None:
        return [tag_id]

    return ["N/A"]


def _cmp_vertex_fecha(v1, v2):
    """
    Criterio para ordenar vértices por fecha de creación ascendente.
    """
    return v1["creation_time"] < v2["creation_time"]



def load_data(control):
    """
    Carga los datos y muestra el reporte (estadísticas + primeros/últimos 5 nodos)
    """
    filename = input("Ingrese el nombre del archivo (Enter para default large): ")
    if not filename:
        filename = "1000_cranes_mongolia_large.csv"

    lg.load_data(control, filename)

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

    vertices_keys = G.vertices(grafo)
    total_vertices = lt.size(vertices_keys)


    lista_vertices_info = lt.new_list()
    for i in range(total_vertices):
        key = lt.get_element(vertices_keys, i)
        info = G.get_vertex_information(grafo, key)
        lt.add_last(lista_vertices_info, info)


    lt.quick_sort(lista_vertices_info, _cmp_vertex_fecha)

    headers = [
        "Identificador único",
        "Posición (lat, lon)",
        "Fecha de creación",
        "Grullas (tags)",
        "Conteo de eventos"
    ]


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

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


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

def lista_to_string(lista):
    n = lt.size(lista)
    if n == 0:
        return "Desconocido"
    elems = []
    for i in range(n):
        elems.append(str(lt.get_element(lista, i)))
    return ", ".join(elems)

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """

    print("\n" + "="*40)
    print("        REQUERIMIENTO 5")
    print("="*40)

    lat1 = float(input("Latitud del punto de origen: "))
    lon1 = float(input("Longitud del punto de origen: "))
    lat2 = float(input("Latitud del punto de destino: "))
    lon2 = float(input("Longitud del punto de destino: "))

    print("\nSeleccione el grafo a utilizar:")
    print("1. Grafo por distancia de desplazamiento")
    print("2. Grafo por distancia a fuentes hídricas")
    opcion = input("Opción (1/2): ").strip()

    if opcion == "2":
        grafo = control["grafo_agua"]
        tipo_grafo = "Grafo hídrico"
    else:
        grafo = control["grafo_distancia"]
        tipo_grafo = "Grafo por distancia"

    punto_origen = (lat1, lon1)
    punto_destino = (lat2, lon2)

    answer = lg.req_5(control, punto_origen, punto_destino, grafo)

    if not answer["ruta_valida"]:
        print("\nNo existe una ruta migratoria viable entre los puntos dados.")
        return

    print(f"\nTipo de grafo usado: {tipo_grafo}")
    print(f"Total de puntos en la ruta: {answer['total_puntos']}")
    print(f"Total de segmentos en la ruta: {answer['total_segmentos']}")

    try:
        costo_str = f"{answer['costo_total']:.3f}"
    except:
        costo_str = str(answer["costo_total"])
    print(f"Costo total de la ruta: {costo_str}")

    headers = [
        "Id punto",
        "Latitud",
        "Longitud",
        "# individuos",
        "3 primeros tags",
        "3 últimos tags",
        "Dist. al siguiente"
    ]

    print("\n--- Primeros 5 puntos de la ruta ---")
    tabla_primeros = []
    primeros = answer["primeros"]
    for i in range(lt.size(primeros)):
        p = lt.get_element(primeros, i)
        try:
            dist_str = f"{p['dist_next']:.3f}"
        except:
            dist_str = str(p["dist_next"])

        fila = [
            p["id"],
            f"{p['lat']:.5f}",
            f"{p['lon']:.5f}",
            p["num_individuos"],
            lista_to_string(p["tags_prim"]),
            lista_to_string(p["tags_ult"]),
            dist_str
        ]
        tabla_primeros.append(fila)

    print(tabulate(tabla_primeros, headers=headers, tablefmt="grid"))

    print("\n--- Últimos 5 puntos de la ruta ---")
    tabla_ultimos = []
    ultimos = answer["ultimos"]
    for i in range(lt.size(ultimos)):
        p = lt.get_element(ultimos, i)
        try:
            dist_str = f"{p['dist_next']:.3f}"
        except:
            dist_str = str(p["dist_next"])

        fila = [
            p["id"],
            f"{p['lat']:.5f}",
            f"{p['lon']:.5f}",
            p["num_individuos"],
            lista_to_string(p["tags_prim"]),
            lista_to_string(p["tags_ult"]),
            dist_str
        ]
        tabla_ultimos.append(fila)

    print(tabulate(tabla_ultimos, headers=headers, tablefmt="grid"))



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
