from DataStructures.List import array_list
from DataStructures.Tree import rbt_node as rbt
from DataStructures.List import single_linked_list as sl


def new_map():
    return {"root": None,
            "type": "RBT"}


def put(my_rbt, key, value):
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    rbt.change_color(my_rbt["root"], rbt.BLACK)
    return my_rbt   


def insert_node(h, key, value):
    if h is None:
        return rbt.new_node(key, value, rbt.RED)
    if key < h["key"]:
        h["left"] = insert_node(h["left"], key, value)
    elif key > h["key"]:
        h["right"] = insert_node(h["right"], key, value)
    else:
        h["value"] = value
    if h["right"] is not None and rbt.is_red(h["right"]) and not (h["left"] is not None and rbt.is_red(h["left"])):
        h = rotate_left(h)
    if h["left"] is not None and rbt.is_red(h["left"]) and h["left"]["left"] is not None and rbt.is_red(h["left"]["left"]):
        h = rotate_right(h)
    if h["left"] is not None and h["right"] is not None and rbt.is_red(h["left"]) and rbt.is_red(h["right"]):
        flip_colors(h)
    h["size"] = 1 + size_nodo(h["left"]) + size_nodo(h["right"])
    return h


def default_compare(key, element):
    resultado=0
    if key < element["key"]:
        resultado=-1
    elif key > element["key"]:
        resultado=1
    else:
        resultado=0
    return resultado


def rotate_left(h):
    x = h["right"]
    h["right"] = x["left"]
    x["left"] = h
    x["color"] = h["color"]
    rbt.change_color(h, rbt.RED)
    x["size"] = h["size"]
    h["size"] = 1 + size_nodo(h["left"]) + size_nodo(h["right"])
    return x


def rotate_right(h):
    x = h["left"]
    h["left"] = x["right"]
    x["right"] = h
    x["color"] = h["color"]
    rbt.change_color(h, rbt.RED)
    x["size"] = h["size"]
    h["size"] = 1 + size_nodo(h["left"]) + size_nodo(h["right"])
    return x


def flip_colors(h):
    flip_node_color(h)
    if h["left"] is not None:
        flip_node_color(h["left"])
    if h["right"] is not None:
        flip_node_color(h["right"])
    return h
        

def flip_node_color(node_rbt):
    if node_rbt is None:
        return None
    if node_rbt["color"] == rbt.RED:
        rbt.change_color(node_rbt, rbt.BLACK)
    else:
        rbt.change_color(node_rbt, rbt.RED)    
    return node_rbt


def is_red(node_rbt):
    if node_rbt is None:
        return False
    return node_rbt["color"] == rbt.RED


def get(my_rbt, key):
    return get_node(my_rbt["root"], key)


def contains(my_rbt, key):
    return get(my_rbt, key) is not None


def size_nodo(node):
    return 0 if node is None else node["size"]


def is_empty(my_rbt):
    return my_rbt["root"] is None


def key_set(my_rbt):
    lista = sl.new_list()
    return key_set_tree(my_rbt["root"], lista)


def value_set(my_rbt):
    lista = sl.new_list()
    return value_set_tree(my_rbt["root"], lista)


def get_min(my_rbt):
    if my_rbt is None or my_rbt["root"] is None:
        return None
    node = get_min_node(my_rbt["root"])
    return node["key"] if node else None


def get_max(my_rbt):
    if my_rbt is None or my_rbt["root"] is None:
        return None
    node = get_max_node(my_rbt["root"])
    return node["key"] if node else None


def height(my_rbt):
    return height_tree(my_rbt["root"])


def keys(my_rbt, key_initial, key_final):
    lista = sl.new_list()
    return keys_range(my_rbt["root"], key_initial, key_final, lista)


def values(my_rbt, key_initial, key_final):
    lista = sl.new_list()
    return values_range(my_rbt["root"], key_initial, key_final, lista)


def size_tree(root):
    if root is None:
        return 0
    return 1 + size_tree(root["left"]) + size_tree(root["right"])


def get_node(root, key):
    if root is None:
        return None
    if key < rbt.get_key(root):
        return get_node(root["left"], key)
    elif key > rbt.get_key(root):
        return get_node(root["right"], key)
    else:
        return rbt.get_value(root)


def key_set_tree(root, lista):
    if root is not None:
        key_set_tree(root["left"], lista)
        sl.add_last(lista, rbt.get_key(root))
        key_set_tree(root["right"], lista)
    return lista


def value_set_tree(root, lista):
    if root is not None:
        value_set_tree(root["left"], lista)
        sl.add_last(lista, rbt.get_value(root))
        value_set_tree(root["right"], lista)
    return lista


def size(my_rbt):
    return size_tree(my_rbt["root"])


def get_min_node(root):
    if root is None:
        return None
    current = root
    while current["left"] is not None:
        current = current["left"]
    return current


def get_max_node(root):
    if root is None:
        return None
    current = root
    while current["right"] is not None:
        current = current["right"]
    return current


def delete_min(my_rbt):
    my_rbt["root"] = delete_min_node(my_rbt["root"])
    return my_rbt


def delete_min_node(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_node(root["left"])
    return root


def delete_max(my_rbt):
    my_rbt["root"]=delete_max_node(my_rbt["root"])
    return my_rbt


def delete_max_node(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"]=delete_max_node(root["right"])
    return root


def height_tree(root):
    if root is None:
        return 0
    left_height = height_tree(root["left"])
    right_height = height_tree(root["right"])
    return 1 + max(left_height, right_height)


def keys_range(root, key_initial, key_final, list_key):
    if root is None:
        return list_key
    key = rbt.get_key(root)
    if key > key_initial:
        keys_range(root["left"], key_initial, key_final, list_key)
    if key_initial <= key <= key_final:
        sl.add_last(list_key, key)
    if key < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)
    return list_key


def values_range(root, key_initial, key_final, lista):
    if root is None:
        return lista
    key = rbt.get_key(root)
    if key > key_initial:
        values_range(root["left"], key_initial, key_final, lista)
    if key_initial <= key <= key_final:
        sl.add_last(lista, rbt.get_value(root))
    if key < key_final:
        values_range(root["right"], key_initial, key_final, lista)
    return lista