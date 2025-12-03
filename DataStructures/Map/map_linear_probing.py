from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as al

import random

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def is_available(table, pos):

   entry = al.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False

def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1

def new_map(num_elements, load_factor, prime=109345121):
    required_capacity = num_elements // load_factor

    if required_capacity < 1:
        required_capacity = 1
    capacity=mf.next_prime(required_capacity)
    table = al.new_list()
    for _ in range(capacity):
        diccionario={
            'key': None,
            'value': None
         }
        al.add_last(table,diccionario)
        
    newmap = {"prime": prime,
              "capacity": capacity,
              "scale": random.randint(1, prime-1),
              "shift": random.randint(0, prime-1),
              "table": table,
              "current_factor": 0,
              "limit_factor": load_factor,
              "size": 0}
    
    return newmap 

def put(my_map, key, value):
    hash_value = mf.hash_value(my_map, key) 
    
    ocupied, slot = find_slot(my_map, key, hash_value)
    entry = al.get_element(my_map["table"], slot)
    entry["key"] = key
    entry["value"] = value  
    if not ocupied:
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        
    if my_map["current_factor"]>=my_map["limit_factor"]:
        my_map=rehash(my_map)
    
    return my_map
def contains(my_map, key):
    if my_map["size"] == 0:
        return False
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    
    return ocupied
def get(my_map, key):
    if my_map["size"] == 0:
        return None
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = my_map["table"]["elements"][slot]
        return entry["value"]
    
    return None
    
def remove(my_map, key):
    if my_map["size"]==0:
        return my_map
    
    hash_value = mf.hash_value(my_map, key)
    ocupied, slot = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = my_map["table"]["elements"][slot]
        entry["key"] = "__EMPTY__"
        entry["value"] = "__EMPTY__"
        my_map["size"] -= 1
        
    return my_map
     
def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    llaves = al.new_list()
    table = my_map["table"]
    
    for posicion in range(my_map["capacity"]):
        entrada = al.get_element(table, posicion)
        if not is_available(table, posicion):
            al.add_last(llaves, me.get_key(entrada))
       
    return llaves

def value_set(my_map):
    valores = al.new_list()
    table = my_map["table"]
    
    for posicion in range(my_map["capacity"]):
        entrada = al.get_element(table, posicion)
        if not is_available(table, posicion):
            al.add_last(valores, me.get_value(entrada))
    
    return valores

def rehash(my_map):
    new_capacity = mf.next_prime(2 * my_map["capacity"])
    new_map_ = new_map(new_capacity, my_map["limit_factor"], my_map["prime"])
    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i)
        key = me.get_key(entry)
        value = me.get_value(entry)
        if key is not None and key != "__EMPTY__":
            hash_value = mf.hash_value(new_map_, key)
            _, pos = find_slot(new_map_, key, hash_value)
            al.change_info(new_map_["table"], pos, me.new_map_entry(key, value))
            new_map_["size"] += 1
    new_map_["current_factor"] = new_map_["size"] / new_map_["capacity"]
    return new_map_