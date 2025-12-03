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
        my_list["firts"]=my_list["first"]["next"]
        my_list["first"]["prev"]=None
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

def exchange(my_list,index1,index2):
    nodo1=""
    nodo2=""
    posición=0
    if index1==0:
        nodo1=my_list["first"]
    elif index1==-1 or index1==int(my_list["size"]-1):
        nodo1=my_list["last"]
    else:
        elemento=my_list["first"]["next"]
        while posición<index1:
            posición+=1
            if posición==index1:
                nodo1=elemento
            else:
                elemento=elemento["next"]
    if index2==0:
        nodo2=my_list["first"]
    elif index2==-1 or index2==int(my_list["size"]-1):
        nodo2=my_list["last"]
    else:
        elemento=my_list["first"]["next"]
        while posición<index2:
            posición+=1
            if posición==index2:
                nodo2=elemento
            else:
                elemento=elemento["next"]
    save_info=nodo1["info"]
    nodo2["info"]=nodo1["info"]
    nodo1["info"]=save_info
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
