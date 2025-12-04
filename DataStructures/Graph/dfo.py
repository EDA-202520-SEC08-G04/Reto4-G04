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

def topological_sort(my_graph):
    
    dfo=depth_first_order(my_graph)
    reverse=dfo["reversepost"]
    topo=lt.new_list()
    
    while not stack.is_empty(reverse):
        lt.add_last(topo, stack.pop(reverse))
        
    return topo