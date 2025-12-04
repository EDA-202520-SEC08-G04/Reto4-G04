from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.List import array_list as lt
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfo_structure as df
def dfs_dfo(my_graph, vertex, dfo):
    mp.put(dfo['marked'], vertex, True)
    
    queue.enqueue(dfo['pre'], vertex)
    
    adj_list=G.adjacents(my_graph, vertex)
    n=lt.size(adj_list)
    
    for i in range(n):
        w=lt.get_element(adj_list, i)
        if not mp.contains(dfo['marked'], w):
            dfs_dfo(my_graph, w, dfo)
            
    queue.enqueue(dfo["post"], vertex)
    
    stack.push(dfo["reversepost"], vertex)
    
def depth_first_order(my_graph):
    vertices=G.vertices(my_graph)
    total=lt.size(vertices)
    
    dfo=df.new_dfo_structure(total)
    
    for i in range(total):
        v=lt.get_element(vertices, i)
        if not mp.contains(dfo["marked"], v):
            dfs_dfo(my_graph, v, dfo)
            
    return dfo

def dfs_topo_cycle(my_graph, v, color, pila, ciclo_flag):
    mp.put(color, v, 1)

    adjs = G.adjacents(my_graph, v)
    n = lt.size(adjs)

    for i in range(n):
        w = lt.get_element(adjs, i)

        if not mp.contains(color, w):
            dfs_topo_cycle(my_graph, w, color, pila, ciclo_flag)
            if ciclo_flag["hay_ciclo"]:
                return
        else:
            estado = mp.get(color, w)
            if estado == 1:  
                ciclo_flag["hay_ciclo"] = True
                return

    mp.put(color, v, 2)
    stack.push(pila, v)


def topological_sort(my_graph):
    vertices = G.vertices(my_graph)
    n = lt.size(vertices)

    color = mp.new_map(num_elements=n, load_factor=0.5)
    pila = stack.new_stack()
    ciclo_flag = {"hay_ciclo": False}

    for i in range(n):
        v = lt.get_element(vertices, i)
        if not mp.contains(color, v):
            dfs_topo_cycle(my_graph, v, color, pila, ciclo_flag)
            if ciclo_flag["hay_ciclo"]:
                break

    if ciclo_flag["hay_ciclo"]:
        return None

    orden = lt.new_list()
    while not stack.is_empty(pila):
        lt.add_last(orden, stack.pop(pila))

    return orden