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
    print("\n" + "="*40)
    print("       SISTEMA DE MIGRACIÓN DE AVES")
    print("="*40)
    print("0. Cargar información")
    print("1. Ejecutar Requerimiento 1")
    print("2. Ejecutar Requerimiento 2")
    print("3. Ejecutar Requerimiento 3")
    print("4. Ejecutar Requerimiento 4")
    print("5. Ejecutar Requerimiento 5")
    print("6. Ejecutar Requerimiento 6")
    print("7. Salir")
    print("="*40)

def load_data(control):
    """
    Carga los datos y muestra el reporte idéntico a la imagen
    """
    filename = input("Ingrese el nombre del archivo (Enter para default large): ")
    if not filename:
        filename = "1000_cranes_mongolia_large.csv"
        
    # Llamada a la lógica
    lg.load_data(control, filename)
    
    # --- 1. ESTADÍSTICAS ---
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
    
    print("\n" + "="*40)
    print("CARGA DE DATOS")
    print("="*40)
    # tablefmt="plain" para que se vea limpio como en la parte superior de tu imagen
    print(tabulate(stats, tablefmt="plain")) 
    print("="*40 + "\n")

    print("DETALLE DE NODOS (VÉRTICES)")
    print("="*40)
    
    # Obtenemos vértices
    vertices = G.vertices(grafo)
    total = lt.size(vertices)
    
    headers = ["Identificador único", "Posición (lat, lon)", "Fecha de creación", "Grullas (tags)", "Conteo de eventos"]

    # --- 2. TABLA PRIMEROS 5 NODOS ---
    print("\n--- Primeros 5 Nodos ---")
    table_data_first = []
    limite_first = 5 if total > 5 else total
    
    for i in range(limite_first):
        key = lt.get_element(vertices, i)
        info = G.get_vertex_information(grafo, key)
        
        pos_str = f"({info['lat']:.5f}, {info['lon']:.5f})"
        fecha_str = str(info['creation_time'])
        # Nota: Si tu lógica no guarda la lista de tags, mostrará vacío. 
        # La imagen muestra [6235], asumimos que info tiene 'tags' o lo simulamos con tag_id inicial
        tags = info.get('tags', [info.get('tag_id', 'N/A')]) 
        
        table_data_first.append([
            info['id'], 
            pos_str, 
            fecha_str, 
            tags, 
            info['event_count']
        ])
        
    print(tabulate(table_data_first, headers=headers, tablefmt="grid"))

    # --- 3. TABLA ÚLTIMOS 5 NODOS ---
    if total > 5:
        print("\n--- Últimos 5 Nodos ---")
        table_data_last = []
        start_index = total - 5
        
        for i in range(start_index, total):
            key = lt.get_element(vertices, i)
            info = G.get_vertex_information(grafo, key)
            
            pos_str = f"({info['lat']:.5f}, {info['lon']:.5f})"
            fecha_str = str(info['creation_time'])
            tags = info.get('tags', [info.get('tag_id', 'N/A')])
            
            table_data_last.append([
                info['id'], 
                pos_str, 
                fecha_str, 
                tags, 
                info['event_count']
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
