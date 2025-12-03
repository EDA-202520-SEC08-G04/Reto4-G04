from DataStructures.Queue import queue as qe
from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st
from DataStructures.Priority_queue import priority_queue as pq
def dijkstra(my_graph, source):
    visited_ht = mp.new_map(num_elements=G.order(my_graph), load_factor=0.5 )
      
    #En este algoritmo se hace todo el mapa en esta misma funcion 
    
    keys_vertex=G.vertices(my_graph)
    
    for key in keys_vertex:
        dis=float('inf')
        
        if key==source:
            dis=0
        mp.put(visited_ht, source, {'marked': False, 'edge_from': None, 'dist_to': dis})
    heap=pq.new_heap()
    pq.insert(heap, 0, source)
    while not pq.is_empty(heap):
        u_key=pq.remove(heap)
        
        dis_u= mp.get(visited_ht, u_key)
        d_u=dis_u['dist_to']   
        
        u_vertex=G.get_vertex(my_graph, u_key)
        adjs=u_vertex['adjacents']
        
        for i in G.adjacents(my_graph, u_key):
            weight_uv=mp.get(adjs, i)['weight']
            
            v_info= mp.get(visited_ht, i)
            d_v= v_info['dist_to']
            
            if d_u != 'inf':
                new_d_v=d_u+weight_uv
                
                if d_v == 'inf' or new_d_v<d_v:
                    mp.put(visited_ht, i,  {'marked': True,
                                            'edge_from': u_key,
                                            'dist_to': new_d_v})
                    if mp.contains(visited_ht, i):
                        pq.improve_priority(heap, new_d_v, i)
                    else:
                        pq.insert(heap, new_d_v, i)
    return visited_ht
    
    
    

def dist_to(key_v, aux_structure):
    
    info=mp.get(aux_structure, key_v)
    if info is None:
        raise Exception ('No existe la llave', key_v)
    return info['dist_to']


def has_path_to(key_v, aux_structure):
    return mp.contains(aux_structure, key_v)

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