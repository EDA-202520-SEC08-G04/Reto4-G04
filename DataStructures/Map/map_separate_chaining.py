from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl

def new_map(num_elements, load_factor, prime=109345121):
    
    capacity = mf.next_prime(num_elements//load_factor)
    table = al.new_list()
    for i in range(capacity):
        single=sl.new_list()
        al.add_last(table,single)
        
    newmap = {"prime": prime,
              "capacity": capacity,
              "scale": 1,
              "shift": 0,
              "table": table,
              "current_factor": 0,
              "limit_factor": load_factor,
              "size": 0}
    
    return newmap
        
def put(my_map, key, value):
   
   
   
   hash_value = mf.hash_value(my_map, key)
   lista = al.get_element(my_map["table"], hash_value)
   actual = lista["first"]
   while actual is not None:
      if actual["info"]["key"] == key:
            
         actual["info"]["value"] = value
         return my_map
      actual = actual["next"]
    
    
   diccionario = {"key": key, "value": value}
   sl.add_first(lista, diccionario)
   my_map["size"] += 1
   my_map["current_factor"] = my_map["size"] / my_map["capacity"]
   if my_map["current_factor"] > my_map["limit_factor"]:
        my_map = rehash(my_map) 
   return my_map   
"""   hash_value=mf.hash_value(my_map,key)
   lista=al.get_element(my_map["table"],hash_value)
   diccionario={"key":key,"value":value}
   if lista["first"] is None:
      sl.add_first(lista,diccionario)
      my_map["size"] += 1
      my_map["current_factor"] = my_map["size"] / my_map["capacity"]
   else:
      sl.add_last(lista,diccionario)
      my_map["size"]+=1

   

   
   return my_map
      
   """
def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1


def contains(my_map,key):
   if my_map["size"] == 0:
      return False
   
   hash_value = mf.hash_value(my_map, key)
   bucket = al.get_element(my_map["table"], hash_value)
   actual = bucket["first"]
   while actual is not None:
      if actual["info"]["key"] == key:
         return True
      actual = actual["next"]
      
   return False 

 
def get(my_map,key):
   if my_map["size"] == 0:
      return None
   
   hash_value = mf.hash_value(my_map, key)
   bucket = al.get_element(my_map["table"], hash_value)
   actual = bucket["first"]
   while actual is not None:
      if actual["info"]["key"] == key:
         return actual["info"]["value"]
      actual = actual["next"]
      
   return None
    
      
def remove(my_map,key):   
    
   if my_map["size"]==0:
      return my_map
   hash_value=mf.hash_value(my_map,key)
   bucket=al.get_element(my_map["table"], hash_value)
   actual=bucket["first"]
   posicion=0
   while actual is not None:
      if actual["info"]["key"]==key:
         sl.delete_element(bucket,posicion)
         my_map["size"]-=1
         return my_map
      posicion+=1
      actual=actual["next"]
   return my_map

def size(my_map):
    return my_map["size"]
 

def is_empty(my_map):
   return my_map["size"] == 0

def key_set(my_map):
   llaves=al.new_list()
   for i in my_map["table"]["elements"]:
      if i["first"]!=None:
         al.add_last(llaves,i["first"]["info"]["key"])
   return llaves

def value_set(my_map):
   valores=al.new_list()
   for i in my_map["table"]["elements"]:
      if i["first"]!=None:
         al.add_last(valores,i["first"]["info"]["value"])
   return valores

def rehash(my_map):
    capacidad = mf.next_prime(my_map["capacity"] * 2)
    nueva_tabla = al.new_list()
    for i in range(capacidad):
        single = sl.new_list()
        al.add_last(nueva_tabla, single)
        
    anterior = my_map["table"]

    my_map["capacity"] = capacidad
    my_map["table"] = nueva_tabla
    my_map["size"] = 0
    my_map["current_factor"] = 0
    
    for lista in anterior["elements"]:
        actual = lista["first"]
        while actual is not None:
            entry = actual["info"]
            put(my_map, entry["key"], entry["value"])
            actual = actual["next"]
    
    return my_map


 
 