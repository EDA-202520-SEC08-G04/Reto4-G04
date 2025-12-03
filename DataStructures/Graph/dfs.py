from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st
from DataStructures.List import array_list as al
def dfs(my_graph, source): #source es la llave con la que se inicia el recorrido
    visited_ht = mp.new_map(num_elements=G.order(my_graph), load_factor=0.5 )
    mp.put(visited_ht, source, {'marked': True, 'edge_from': None})  
    dfs_vertex(my_graph, source, visited_ht)
    return visited_ht

def dfs_vertex(my_graph, vertex, visited_map):
    pila=st.new_stack()
    st.push(pila, vertex)
    while not st.is_empty(pila):
        x_ver=st.pop(pila)
        adj_keys=G.adjacents(my_graph, x_ver)
        for i in adj_keys:
            if not mp.contains(visited_map, i):
                st.push(pila, i)
                mp.put(visited_map, i,{'marked': True, 'edge_from': x_ver})
    pass  #no hay retorno
def has_path_to(key_v, visited_map):
    return mp.contains(visited_map, key_v)
    
def path_to(key_v, visited_map):
    
    if not has_path_to(key_v, visited_map):
        return None
    
    
    stack= st.new_stack()
    path=al.new_list()
    vertex=key_v
    
    while vertex is not None:
        v=mp.get(visited_map, vertex)
        st.push(stack, vertex)
        vertex=v['edge_from']    
    
    while not st.is_empty(stack):
        al.add_last(path, st.pop(stack))    
    return path

