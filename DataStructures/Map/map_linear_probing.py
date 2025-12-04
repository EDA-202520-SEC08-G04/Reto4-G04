import random
from DataStructures.Map import map_functions as mf

def new_map(num_elements, load_factor, prime=109345121):
    required_capacity = num_elements // load_factor
    if required_capacity < 1:
        required_capacity = 1
    
    capacity = mf.next_prime(required_capacity)
    
    # OPTIMIZACIÓN: Usar lista Python directa en lugar de array_list
    table = [{"key": None, "value": None} for _ in range(capacity)]
    
    newmap = {
        "prime": prime,
        "capacity": capacity,
        "scale": random.randint(1, prime-1),
        "shift": random.randint(0, prime-1),
        "table": table,  # Lista Python directa
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0
    }
    
    return newmap


def is_available(table, pos):
    """OPTIMIZADO: Acceso directo sin wrapper"""
    entry = table[pos]
    key = entry["key"]
    return key is None or key == "__EMPTY__"


def default_compare(key, entry):
    """Compara una key con la key de un entry"""
    entry_key = entry["key"]
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1


def find_slot(my_map, key, hash_value):
    """OPTIMIZADO: Acceso directo a tabla"""
    table = my_map["table"]
    capacity = my_map["capacity"]
    first_avail = None
    found = False
    ocupied = False
    
    # OPTIMIZACIÓN: Límite de iteraciones para evitar loops infinitos
    max_iterations = capacity
    iterations = 0
    
    while not found and iterations < max_iterations:
        iterations += 1
        entry = table[hash_value]  # Acceso directo O(1)
        
        if is_available(table, hash_value):
            if first_avail is None:
                first_avail = hash_value
            if entry["key"] is None:
                found = True
        elif key == entry["key"]:  # Comparación directa
            first_avail = hash_value
            found = True
            ocupied = True
        
        hash_value = (hash_value + 1) % capacity
    
    return ocupied, first_avail


def put(my_map, key, value):
    """OPTIMIZADO: Sin conversiones innecesarias"""
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    
    if slot is None:
        return my_map  # Tabla llena (no debería pasar)
    
    # Acceso directo
    my_map["table"][slot]["key"] = key
    my_map["table"][slot]["value"] = value
    
    if not ocupied:
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    
    # Rehash si es necesario
    if my_map["current_factor"] >= my_map["limit_factor"]:
        my_map = rehash(my_map)
    
    return my_map


def contains(my_map, key):
    """OPTIMIZADO: Verificación rápida"""
    if my_map["size"] == 0:
        return False
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    
    return ocupied


def get(my_map, key):
    """OPTIMIZADO: Acceso directo"""
    if my_map["size"] == 0:
        return None
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    
    if ocupied and slot is not None:
        return my_map["table"][slot]["value"]
    
    return None


def remove(my_map, key):
    """Elimina un elemento del map"""
    if my_map["size"] == 0:
        return my_map
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    
    if ocupied and slot is not None:
        my_map["table"][slot]["key"] = "__EMPTY__"
        my_map["table"][slot]["value"] = None
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    
    return my_map


def size(my_map):
    """Retorna el número de elementos"""
    return my_map["size"]


def is_empty(my_map):
    """Verifica si el map está vacío"""
    return my_map["size"] == 0


def key_set(my_map):
    """OPTIMIZADO: Retorna lista de keys sin usar array_list"""
    from DataStructures.List import array_list as al
    
    keys = al.new_list()
    table = my_map["table"]
    
    for entry in table:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            al.add_last(keys, entry["key"])
    
    return keys


def value_set(my_map):
    """OPTIMIZADO: Retorna lista de valores"""
    from DataStructures.List import array_list as al
    
    values = al.new_list()
    table = my_map["table"]
    
    for entry in table:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            al.add_last(values, entry["value"])
    
    return values


def rehash(my_map):
    """OPTIMIZADO: Rehashing eficiente"""
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]
    
    # Nueva capacidad
    new_capacity = mf.next_prime(old_capacity * 2)
    
    # Crear nueva tabla
    new_table = [{"key": None, "value": None} for _ in range(new_capacity)]
    
    # Actualizar mapa
    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0
    my_map["scale"] = random.randint(1, my_map["prime"]-1)
    my_map["shift"] = random.randint(0, my_map["prime"]-1)
    
    # Re-insertar elementos
    for entry in old_table:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            put(my_map, entry["key"], entry["value"])
    
    return my_map