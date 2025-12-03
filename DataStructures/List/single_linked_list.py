from . import list_node as ln
def new_list():
    newlist={
        "size":0,
        "first":None,
        "last":None,    
    }
    return newlist


def get_element(my_list,pos):
    searchpos=0
    node=my_list["first"]
    while searchpos<pos:
        node=node["next"]
        searchpos +=1
    return node["info"]


def cmp_function(a, b):
    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1
    
    
def is_present(my_list, element, cmp_function):
    is_in_array =False
    temp=my_list["first"]
    count=0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"])==0:
            is_in_array=True
        else:
            temp =temp["next"]
            count +=1
    if not is_in_array:
        count  = -1
    return count 


def add_first(my_list,element):
    if my_list["first"]==None:
        nodo=ln.new_double_node(element)
        my_list["first"]=nodo
        my_list["last"]=nodo    
    else:
        nodo=ln.new_double_node(element)
        nodo["next"]=my_list["first"]
        my_list["first"]["prev"]=nodo
        my_list["first"]=nodo
    my_list["size"]+=1    
    return my_list


def add_last(my_list,element):
    if my_list["first"]==None:
        add_first(my_list,element)
        return my_list
    else:
        nodo=ln.new_double_node(element)
        nodo["prev"]=my_list["last"]
        my_list["last"]["next"]=nodo
        my_list["last"]=nodo
    if my_list["size"]==1:
        my_list["first"]["next"]=my_list["last"]
    my_list["size"]+=1
    return my_list


def is_empty(my_list):
    if my_list["size"]==0:
        retorno=True
    else:
        retorno=False
    return retorno


def size(my_list):
    return my_list["size"]


def first_element(my_list):
    if my_list["size"]==0:
        raise IndexError("list index out of range")
    else:
        retorno=my_list["first"]
    return retorno


def last_element(my_list):
    if my_list["size"]==0:
        raise IndexError("list index out of range")
    else:
        retorno=my_list["last"]
    return retorno


def remove_first(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")

    node = my_list["first"]
    value = node["info"]

    if my_list["size"] == 1:
        my_list["first"] = None
        my_list["last"]  = None
    else:
        new_first = node["next"]
        new_first["prev"] = None
        my_list["first"] = new_first
        node["next"] = None 

    my_list["size"] -= 1
    return value

        
def remove_last(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")

    node = my_list["last"]
    value = node["info"]

    if my_list["size"] == 1:
        my_list["first"] = None
        my_list["last"]  = None
    else:
        new_last = node["prev"]
        new_last["next"] = None
        my_list["last"] = new_last
        node["prev"] = None 

    my_list["size"] -= 1
    return value


def insert_element(my_list,element,index):
    place=0
    if my_list["size"]==0:
        add_first(my_list,element)
    elif int(index)==-1:
        add_last(my_list,element)
    else:
        elemento=my_list["first"]
        while place<index:
            place+=1
            nodo=ln.new_double_node(element)
            if place==int(index):
                next=elemento["next"]
                nodo["next"]=next
                nodo["prev"]=elemento
                elemento["next"]=nodo
                next["prev"]=nodo
            else:
                elemento=elemento["next"]
        my_list["size"]+=1       
    return my_list 


def delete_element(my_list,pos):
    place = 0
    elemento = my_list["first"]
    if pos==0:
        my_list["first"] = my_list["first"]["next"]
        if my_list["first"] is not None: 
            my_list["first"]["prev"] = None
    if pos>my_list["size"]-1:
        raise IndexError("list index out of range")
    while place < pos:
        elemento = elemento["next"]
        place += 1

    if elemento["next"] is not None: 
        elemento["next"]["prev"] = elemento["prev"]
    if elemento["prev"] is not None: 
        elemento["prev"]["next"] = elemento["next"]
    my_list["size"]-=1
    return elemento


def change_info(my_list,index,new_info):
    elemento=my_list["first"]
    place=-1
    while place<index:
        place+=1
        if place==index:
            elemento["info"]=new_info   
        else:
            elemento=elemento["next"]
    return my_list


def exchange(my_list, index1, index2):
    nodo1 = ""
    nodo2 = ""
    posicion = 0
    if index1 == 0:
        nodo1 = my_list["first"]
    elif index1 == -1 or index1 == int(my_list["size"] - 1):
        nodo1 = my_list["last"]
    else:
        elemento = my_list["first"]["next"]
        while posicion < index1:
            posicion += 1
            if posicion == index1:
                nodo1 = elemento
            else:
                elemento = elemento["next"]
    posicion = 0
    if index2 == 0:
        nodo2 = my_list["first"]
    elif index2 == -1 or index2 == int(my_list["size"] - 1):
        nodo2 = my_list["last"]
    else:
        elemento = my_list["first"]["next"]
        while posicion < index2:
            posicion += 1
            if posicion == index2:
                nodo2 = elemento
            else:
                elemento = elemento["next"]
    save_info = nodo1["info"]
    nodo1["info"] = nodo2["info"]
    nodo2["info"] = save_info
    return my_list


def sub_list(my_list,start,end):
    lista=""
    posición=0
    if end>my_list["size"]-1:
        raise IndexError("list index out of range")
    else:
        elemento=my_list["first"]
        if start==0:
            lista=elemento
        else:
            while posición<start:
                posición+=1
                if posición==start:
                    lista=elemento
                else:
                    elemento=elemento["next"]
    elemento=lista
    while posición<end:
        posición+=1
        if posición==end:
            lista["next"]=None
        else:
            elemento=elemento["next"]
    return lista


def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

           
def selection_sort(my_list, sort_criteria=default_sort_criteria):
    if my_list["size"] <= 1:
        return my_list
    current = my_list["first"]
    i = 0
    while current is not None and i < my_list["size"] - 1:
        next_node = current["next"]
        j = i + 1
        min_index = i
        while next_node is not None and j < my_list["size"]:
            if sort_criteria(next_node["info"], get_element(my_list, min_index)):
                min_index = j
            next_node = next_node["next"]
            j += 1
        if min_index != i:
            exchange(my_list, i, min_index)
        current = current["next"]
        i += 1
    return my_list


def insertion_sort(my_list, sort_criteria=default_sort_criteria):
    if my_list["size"] <= 1:
        return my_list

    actual_pos = 1
    while actual_pos < my_list["size"]:
        j = actual_pos
        while j > 0:
            actual_info = get_element(my_list, j)
            prev_info = get_element(my_list, j - 1)
            if sort_criteria(actual_info, prev_info):
                exchange(my_list, j, j - 1)
                j -= 1
            else:
                j=0
        actual_pos += 1
    return my_list
 
       
def shell_sort(my_list, sort_criteria=default_sort_criteria):
    
    if my_list["size"] >1:
        size = my_list["size"]
        intervalo = 1
        
        while intervalo < size //3:
            intervalo = 3 * intervalo + 1
            
        while intervalo >= 1:
            i = intervalo
            while i < size:
                j = i
                while (j >= intervalo and sort_criteria(get_element(my_list, j), get_element(my_list, j - intervalo))):
                    exchange(my_list, j, j - intervalo)
                    j -= intervalo
                i += 1
            intervalo //= 3
    
    return my_list


def dividir_lista(cabeza):
    lento = cabeza
    rapido = cabeza

    while rapido is not None and rapido["next"] is not None:
        rapido = rapido["next"]["next"] if rapido["next"] is not None else None
        if rapido is not None:
            lento = lento["next"]

    segunda_mitad = lento["next"]
    lento["next"] = None
    if segunda_mitad is not None:
        segunda_mitad["prev"] = None

    return cabeza, segunda_mitad

def combinar_listas(lista1, lista2, criterio):
    if lista1 is None:
        return lista2
    if lista2 is None:
        return lista1

    nodo_temporal = ln.new_double_node(None)
    ultimo = nodo_temporal
    nodo1, nodo2 = lista1, lista2

    while nodo1 is not None and nodo2 is not None:
        if criterio(nodo1["info"], nodo2["info"]):
            ultimo["next"] = nodo1
            nodo1["prev"] = ultimo
            nodo1 = nodo1["next"]
        else:
            ultimo["next"] = nodo2
            nodo2["prev"] = ultimo
            nodo2 = nodo2["next"]
        ultimo = ultimo["next"]

    sobrantes = nodo1 if nodo1 is not None else nodo2
    if sobrantes is not None:
        ultimo["next"] = sobrantes
        sobrantes["prev"] = ultimo

    cabeza_final = nodo_temporal["next"]
    if cabeza_final is not None:
        cabeza_final["prev"] = None
    nodo_temporal["next"] = None
    return cabeza_final

def merge_sort_nodos(cabeza, criterio):
    if cabeza is None or cabeza["next"] is None:
        return cabeza

    primera_mitad, segunda_mitad = dividir_lista(cabeza)
    primera_ordenada = merge_sort_nodos(primera_mitad, criterio)
    segunda_ordenada = merge_sort_nodos(segunda_mitad, criterio)

    return combinar_listas(primera_ordenada, segunda_ordenada, criterio)

def reconstruir_lista(mi_lista, cabeza):
    nodo = cabeza
    anterior = None
    contador = 0

    while nodo is not None:
        nodo["prev"] = anterior
        anterior = nodo
        nodo = nodo["next"]
        contador += 1

    mi_lista["first"] = cabeza
    mi_lista["last"] = anterior
    mi_lista["size"] = contador
    return mi_lista

def merge_sort(mi_lista, criterio=default_sort_criteria):
    if mi_lista["size"] <= 1 or mi_lista["first"] is None:
        return mi_lista

    cabeza_ordenada = merge_sort_nodos(mi_lista["first"], criterio)
    return reconstruir_lista(mi_lista, cabeza_ordenada)


def menor(a, b, criterio):
    return criterio(a, b) and not criterio(b, a)

def mayor(a, b, criterio):
    return criterio(b, a) and not criterio(a, b)

def agregar_al_final(primero, ultimo, nodo):
    nodo["prev"] = ultimo
    nodo["next"] = None
    if ultimo is None:
        primero = ultimo = nodo
    else:
        ultimo["next"] = nodo
        ultimo = nodo
    return primero, ultimo

def concatenar_listas(p1_primero, p1_ultimo, p2_primero, p2_ultimo):
    if p1_primero is None:
        return p2_primero, p2_ultimo
    if p2_primero is None:
        return p1_primero, p1_ultimo
    p1_ultimo["next"] = p2_primero
    p2_primero["prev"] = p1_ultimo
    return p1_primero, p2_ultimo

def quick_sort_nodos(cabeza, criterio):
    if cabeza is None or cabeza["next"] is None:
        return cabeza, cabeza

    pivote_valor = cabeza["info"]

    menos_primero = menos_ultimo = None
    igual_primero = igual_ultimo = None
    mas_primero = mas_ultimo = None

    nodo = cabeza
    while nodo is not None:
        siguiente = nodo["next"]
        nodo["prev"] = nodo["next"] = None

        if menor(nodo["info"], pivote_valor, criterio):
            menos_primero, menos_ultimo = agregar_al_final(menos_primero, menos_ultimo, nodo)
        elif mayor(nodo["info"], pivote_valor, criterio):
            mas_primero, mas_ultimo = agregar_al_final(mas_primero, mas_ultimo, nodo)
        else:
            igual_primero, igual_ultimo = agregar_al_final(igual_primero, igual_ultimo, nodo)

        nodo = siguiente

    menos_primero, menos_ultimo = quick_sort_nodos(menos_primero, criterio) if menos_primero else (None, None)
    mas_primero, mas_ultimo = quick_sort_nodos(mas_primero, criterio) if mas_primero else (None, None)

    cabeza_temp, cola_temp = concatenar_listas(menos_primero, menos_ultimo, igual_primero, igual_ultimo)
    cabeza_final, cola_final = concatenar_listas(cabeza_temp, cola_temp, mas_primero, mas_ultimo)

    return cabeza_final, cola_final

def quick_sort(mi_lista, criterio=default_sort_criteria):
    if mi_lista["size"] <= 1 or mi_lista["first"] is None:
        return mi_lista

    cabeza_ordenada, cola_ordenada = quick_sort_nodos(mi_lista["first"], criterio)

    nodo = cabeza_ordenada
    contador = 0
    while nodo is not None:
        contador += 1
        nodo = nodo["next"]

    mi_lista["first"] = cabeza_ordenada
    mi_lista["last"] = cola_ordenada
    mi_lista["size"] = contador
    return mi_lista

    
    


                