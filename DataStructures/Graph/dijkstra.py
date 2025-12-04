from DataStructures.Queue import queue as qe
from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st
from DataStructures.Priority_queue import priority_queue as pq
def dijkstra(my_graph, source):
    visited_ht = mp.new_map(num_elements=G.order(my_graph), load_factor=0.5)
    keys_vertex = G.vertices(my_graph)
    INF = float('inf')

    for i in range(al.size(keys_vertex)):
        key = al.get_element(keys_vertex, i)
        dis = 0 if key == source else INF
        mp.put(visited_ht, key, {'marked': False, 'edge_from': None, 'dist_to': dis})

    heap = pq.new_heap()
    pq.insert(heap, 0, source)

    while not pq.is_empty(heap):
        u_key = pq.remove(heap)
        u_info = mp.get(visited_ht, u_key)
        d_u = u_info['dist_to']

        if d_u == INF:
            continue

        u_vertex = G.get_vertex(my_graph, u_key)
        adjs = u_vertex['adjacents']
        adj_keys = G.adjacents(my_graph, u_key)

        for j in range(al.size(adj_keys)):
            v_key = al.get_element(adj_keys, j)
            weight_uv = mp.get(adjs, v_key)
            v_info = mp.get(visited_ht, v_key)
            d_v = v_info['dist_to']
            new_d_v = d_u + weight_uv

            if new_d_v < d_v:
                mp.put(visited_ht, v_key, {
                    'marked': True,
                    'edge_from': u_key,
                    'dist_to': new_d_v
                })
                pq.insert(heap, new_d_v, v_key)

    return visited_ht


def dist_to(key_v, aux_structure):
    
    info=mp.get(aux_structure, key_v)
    if info is None:
        raise Exception ('No existe la llave', key_v)
    return info['dist_to']


def has_path_to(key_v, aux_structure):
    info = mp.get(aux_structure, key_v)
    if info is None:
        return False
    return info["dist_to"] != float('inf')
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