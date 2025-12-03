from DataStructures.Tree import bst_node as bst
from DataStructures.List import single_linked_list as sl

def new_map():
    return {"root":None}

def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def insert_node(node, key, value):
    
    if node is None:
        return bst.new_node(key, value)
    if node["key"]==key:
        node["value"]=value
        return node 
    if node["key"]>key:
        if node["left"] is None:
            node["left"]=bst.new_node(key, value)
        else:
            node["left"]=insert_node(node["left"], key, value)
            
    else:
        if node["right"] is None:
            node["right"]=bst.new_node(key, value)
        else:
            node["right"]=insert_node(node["right"], key, value)
        
    left_size=0
    right_size=0
    if node["left"] is not None:
        left_size=node["left"]["size"]
    if node["right"] is not None:
        right_size=node["right"]["size"]
    node["size"]=1+left_size+right_size
    
    return node 
def get(my_bst, key):
    retorno=get_node(my_bst["root"], key)
    if retorno is not None:
        return retorno["value"]
    return None


def get_node(node, key):
    if node is None:
        return None
    if node["key"]==key:
        return node
    elif node["key"]>key:
        return get_node(node["left"], key)
    else:
        return get_node(node["right"], key)
    
    
def size(my_bst):
    if my_bst['root'] is not None:
        return size_tree(my_bst["root"])
    return 0

def size_tree(root):
    if root is None:
        return 0
    return int(root["size"])
    
def contains(my_bst, key):
    return get(my_bst, key) is not None


def is_empty(my_bst):
    return my_bst["root"] is None



def key_set(my_bst):
    lista=sl.new_list()
    if is_empty(my_bst):
        return lista
    return key_set_tree(my_bst['root'], lista)
    
    
def key_set_tree(node,lst):
    if node is None:
        return lst
    else:
        sl.add_last(lst, node["key"])
        key_set_tree(node['left'], lst)
        key_set_tree(node['right'], lst)
        return lst
    
def value_set(my_bst):
    lista=sl.new_list()
    if is_empty(my_bst):
        return lista
    return value_set_tree(my_bst['root'], lista)
    
    
def value_set_tree(node,lst):
    if node is None:
        return lst
    else:
        sl.add_last(lst, node["value"])
        value_set_tree(node['left'], lst)
        value_set_tree(node['right'], lst)
        return lst
    
def get_min(my_bst):
    if is_empty(my_bst):
        return None
    return get_min_node(my_bst['root'])

def get_min_node(node):
    if node['left'] is not None:
        return get_min_node(node['left'])
    return node['key']

def get_max(my_bst):
    if is_empty(my_bst):
        return None
    return get_max_node(my_bst['root'])

def get_max_node(node):
    if node['right'] is not None:
        return get_max_node(node['right'])
    return node['key']

def delete_min(my_bst):
    if is_empty(my_bst):
        return my_bst
    my_bst['root']=delete_min_tree(my_bst['root'])
    return my_bst

def delete_min_tree(node):
    if node is None:
        return None
    if node['left'] is None:
        return node['right']
    node['left']=delete_min_tree(node['left'])
    node['size']=1+size_tree(node['left'])+size_tree(node['right'])
    
    return node

def delete_max(my_bst):
    if is_empty(my_bst):
        return my_bst
    my_bst['root']=delete_max_tree(my_bst['root'])
    return my_bst

def delete_max_tree(node):
    if node is None:
        return None
    if node['right'] is None:
        return node['left']
    node['right']=delete_max_tree(node['right'])
    node['size']=1+size_tree(node['right'])+size_tree(node['left'])
    
    return node 
 
def height(tree):
    if tree["root"] is not None:
        return get_height(tree["root"])
    else:
        return 0
 
def get_height(tree):
    if tree["left"]!=None and tree["right"]!=None:
        return 1+max(get_height(tree["left"]),get_height(tree["right"]))
    elif tree["left"] is not None:
        return 1+get_height(tree["left"])
    elif tree["right"] is not None:
        return 1+get_height(tree["right"])
    else: 
        return 1
    
    
def keys(tree, inicio, fin):
    lista = sl.new_list()
    if tree["root"] is not None:
        keys_range(tree["root"], inicio, fin, lista)
        return lista
    else:
        return lista

def keys_range(node, inicio, fin, lista):
    if node is None:
        return

    keys_range(node["left"], inicio, fin, lista)

    if inicio <= node["key"] <= fin:
        sl.add_last(lista, node["key"])

    keys_range(node["right"], inicio, fin, lista)

def values(tree, inicio, fin):
    lista = sl.new_list()
    if tree["root"] is not None:
        values_range(tree["root"], inicio, fin, lista)
    return lista


def values_range(node, inicio, fin, lista):
    if node is None:
        return

    values_range(node["left"], inicio, fin, lista)

    if inicio <= node["key"] <= fin:
        sl.add_last(lista, node["value"])

    values_range(node["right"], inicio, fin, lista)