from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.Priority_queue import pq_entry as pe 


def default_compare_higher_value(father_node, child_node):
    if pe.get_priority(father_node) >= pe.get_priority(child_node):
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pe.get_priority(father_node) <= pe.get_priority(child_node):
        return True
    return False

def exchange(my_heap, pos1, pos2):
    al.exchange(my_heap["elements"], pos1, pos2)
    return my_heap

def priority(my_heap, parent, child):
    return my_heap["cmp_function"](parent, child)

def size(my_heap):
    return my_heap["size"]

def is_empty(my_heap):
    return size(my_heap) == 0

def swim(my_heap, pos):
    root = 1
    x = True
    while (pos != root) and x:
        posicion = pos // 2
        parent = al.get_element(my_heap["elements"], posicion)
        child = al.get_element(my_heap["elements"], pos)
        
        if priority(my_heap, child, parent):
            exchange(my_heap, posicion, pos)
            pos = posicion
        else:
            x = False

def insert(my_heap, priority, value):
     nueva_entrada = pe.new_pq_entry(priority, value)
     al.add_last(my_heap["elements"], nueva_entrada)
     my_heap["size"] += 1
     pos = my_heap["size"]
     swim(my_heap, pos)
     return my_heap

def sink(my_heap, pos):
    tamano = my_heap["size"]
    x = True
    while (2 * pos <= tamano) and x:
        izq = 2 * pos
        der = izq + 1
        mejor = izq
        
        if der <= tamano:
            hijo_izq = al.get_element(my_heap["elements"], izq)
            hijo_der = al.get_element(my_heap["elements"], der)
            if priority(my_heap, hijo_der, hijo_izq):
                mejor = der
        
        padre = al.get_element(my_heap["elements"], pos)
        hijo = al.get_element(my_heap["elements"], mejor)
        
        if priority(my_heap, hijo, padre):
            exchange(my_heap, pos, mejor)
            pos = mejor
        else:
            x = False

def remove(my_heap):
    if my_heap["size"] == 0:
        return None

    primero = al.get_element(my_heap["elements"], 1)
    ultimo = al.get_element(my_heap["elements"], my_heap["size"])
    al.change_info(my_heap["elements"], 1, ultimo)
    al.delete_element(my_heap["elements"], my_heap["size"])
    my_heap["size"] -= 1

    if my_heap["size"] > 0:
        sink(my_heap, 1)
    return pe.get_value(primero)

def get_first_priority(my_heap):
    if my_heap["size"] == 0:
        return None

    primero = al.get_element(my_heap["elements"], 1)
    return pe.get_value(primero)

def is_present_value(my_heap, value):
    tamano = my_heap["size"]

    for i in range(1, tamano + 1):
        entrada = al.get_element(my_heap["elements"], i)
        valor_actual = pe.get_value(entrada)

        if valor_actual == value:
            return i  
    return -1

def contains(my_heap, value):
    posicion = is_present_value(my_heap, value)

    if posicion != -1:
        return True
    else:
        return False

def improve_priority(my_heap, priority, value):
    pos = is_present_value(my_heap, value)

    if pos == -1:
        return my_heap
    entrada = al.get_element(my_heap["elements"], pos)
    pe.set_priority(entrada, priority)
    al.change_info(my_heap["elements"], pos, entrada)
    swim(my_heap, pos)
    return my_heap

def new_heap(is_min_pq=True):
    elementos = al.new_list()
    al.add_last(elementos, None)
    
    if is_min_pq:
        cmp_funcion = default_compare_lower_value
    else:
        cmp_funcion = default_compare_higher_value
    heap = {"elements": elementos,
            "size": 0,
            "cmp_function": cmp_funcion}
    
    return heap