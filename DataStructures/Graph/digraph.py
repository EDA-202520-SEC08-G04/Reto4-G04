from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import vertex as vx
from DataStructures.Graph import edge as ed
def new_graph(order):
    vertices=mp.new_map(order, 0.5)
    num_edges=0
    return {'vertices':vertices,
            'num_edges':num_edges}
    
    
    
def insert_vertex(my_graph, key_u, info_u):
    mp.put(my_graph['vertices'], key_u, info_u)
    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    grafo=my_graph['vertices']
    
    ver_u=mp.contains(grafo, key_u)
    ver_v=mp.contains(grafo, key_v)
    if ver_u==False:
        raise Exception ('el vertice u no existe')
    if ver_v==False:
        raise Exception ('el vertice v no existe')
    principal=mp.get(grafo, key_u)
    secundario=principal['adjacents']
    existence=mp.contains(secundario , key_v)
    mp.put(secundario, key_v, weight)
    if not existence:
        my_graph['num_edges']+=1
    return my_graph


def contains_vertex(my_graph, key_u):
    grafo=my_graph['vertices']
    return mp.contains(grafo, key_u)


def order(my_graph):
    return mp.size(my_graph['vertices'])


def size(my_graph):   #este size es tamano pero de arcos
    return my_graph['num_edges']

def degree(my_graph, key_u):
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        raise Exception ('El vertice no existe')
    vertex_to_search=mp.get(graph, key_u)
    adjacent=vertex_to_search['adjacents']
    return mp.size(adjacent)  #adjacentes no tiene num_edges, pero si hay elemento en adjacent, significa que hay arco, por eso el mp.size

def adjacents(my_graph, key_u):
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        raise Exception ('El vertice no existe')
    vertex=mp.get(graph, key_u)
    adjacent=vertex['adjacents']
    adj_keys=mp.key_set(adjacent)
    return adj_keys

def vertices(my_graph):
    #Retorna una lista con las llaves de todos los vertices del grafo my_graph
    graph=my_graph['vertices']
    return mp.key_set(graph)

def edges_vertex(my_graph, key_u):
    #Retorna una lista con todos los arcos asociados a los vértices adyacentes del vertice con llave key_u.
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        raise Exception ('El vertice no existe')   
    vertex_to_search=mp.get(graph, key_u)
    adjacent=vertex_to_search['adjacents']
    edges_list=mp.value_set(adjacent)  
    return edges_list

def get_vertex(my_graph, key_u):
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        return None
    vertex=mp.get(graph, key_u)
    return vertex

def update_vertex_info(my_graph, key_u, new_info_u):
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        return my_graph
    vertex=mp.get(graph, key_u)
    vertex['value']=new_info_u
    return my_graph

def get_vertex_information(my_graph, key_u):
    graph=my_graph['vertices']
    if not contains_vertex(my_graph, key_u):
        raise Exception ('El vertice no existe') 
    return mp.get(graph, key_u)['value']