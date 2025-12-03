def new_list():
    newlist = {
        'elements':[],
        'size':0,
                        
    }
    return newlist


def get_element(my_list,index):
    return my_list["elements"][index]

def is_present(my_list, element,cmp_function):
    size= my_list["size"]
    if size>0:
        keyexist =False
        for keypos in range (0, size):
            info =my_list["elements"][keypos]
            if cmp_function(element,info)==0:
                keyexist =True
                break
        if keyexist:
            return keypos
    return -1



def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"]+=1
    return my_list


def add_last(my_list, element):   
    my_list["elements"].append(element)
    my_list["size"]+=1
    return my_list

def size(my_list):
    return my_list["size"]


def first_element(my_list):
    if my_list["size"]==0:
        raise IndexError("list index out of range")
    return my_list["elements"][0]



def is_empty(my_list):
    return my_list["size"]==0
    

def last_element(my_list):
    if my_list["size"]==0:
        raise IndexError("list index out of range") 
    return my_list["elements"][my_list["size"]-1]



def delete_element(my_list, pos):
    if 0<= pos <my_list["size"]:
        my_list["elements"].pop(pos)
        my_list["size"]-=1
        return my_list 
    else:
        raise IndexError("list index out of range")      
    


def remove_first(my_list):
    if size(my_list)==0:
        raise IndexError("List index out of range")
    my_list["size"]-=1
    return my_list["elements"].pop(0)
    



def remove_last(my_list):
    if size(my_list)==0:
        raise IndexError("list index out of range")
    my_list["size"]-=1
    return my_list["elements"].pop()
    



def insert_element(my_list, element, pos):
    if size(my_list)==0:
        return add_first(my_list, element)
    if pos<=size(my_list):
        my_list["elements"].insert(pos, element)
        my_list["size"]+=1
        return my_list
    else:
        return add_last(my_list, element)


def change_info(my_list, pos, new_info):
    if 0<=pos<size(my_list):
        my_list["elements"][pos]=new_info
        return my_list
    else:
        raise IndexError("list index out of range") 
    



def exchange(my_list,pos1,pos2):

    if 0<=pos1<size(my_list) and 0<=pos2<size(my_list):
        epos1=my_list["elements"][pos1]
        my_list["elements"][pos1]=my_list["elements"][pos2]
        my_list["elements"][pos2]=epos1
        return my_list
    else:
        raise IndexError("list index out of range")



def sub_list(my_list, pos_i, num_elements):
    if 0<=pos_i<size(my_list) and num_elements>=0 and pos_i+num_elements<=size(my_list):
        slist={"elements":[],
               "size":0}
        slist["elements"]=my_list["elements"][pos_i:pos_i+num_elements]
        slist["size"] = len(slist["elements"])
        return slist

    else:
        raise IndexError("list index out of range")
    
def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted


def selection_sort(my_list, sort_criteria=default_sort_criteria):
    size=my_list["size"]
    for i in range(size):
        index=i
        for j in range(i+1, size):    
            if sort_criteria(my_list["elements"][i], my_list["elements"][j])==False:
                index=j
            if index!=i:
                exchange(my_list, i, index)
    return my_list


def insertion_sort(my_list, sort_criteria=default_sort_criteria):
    size=my_list["size"]
    
    for i in range(1, size):
        j=i
        while  j>0 and sort_criteria(my_list["elements"][j], my_list["elements"][j-1]):
            exchange(my_list, j-1, j)
            j-=1
    return my_list


def shell_sort(my_list, sort_criteria=default_sort_criteria):
    
    if my_list["size"]>1:
        n= my_list["size"]
        h=1
        
        while h < n//3:
            h =3*h + 1
        while h>=1:
            for i in range(h, n):
                j=i
                while (j>=h and sort_criteria(get_element(my_list, j), get_element(my_list, j-h))):
                    exchange(my_list, j, j-h)
                    j -=h
            h//=3
    return my_list


def merge_sort(lista, criterio=default_sort_criteria):
    
    tamaño = lista["size"]
    if tamaño <= 1:
        return lista  

    elementos = lista["elements"]
    auxiliar = elementos[:]  

    def merge_sort_recursive(arr, aux, inicio, fin):
        if inicio >= fin:
            return

        medio = (inicio + fin) // 2

        merge_sort_recursive(arr, aux, inicio, medio)
        merge_sort_recursive(arr, aux, medio + 1, fin)
        merge(arr, aux, inicio, medio, fin)

    def merge(arr, aux, inicio, medio, fin):
        aux[inicio:fin + 1] = arr[inicio:fin + 1]

        izquierda = inicio
        derecha = medio + 1

        for k in range(inicio, fin + 1):
            if izquierda > medio:
                arr[k] = aux[derecha]
                derecha += 1
            elif derecha > fin:
                arr[k] = aux[izquierda]
                izquierda += 1
            elif criterio(aux[izquierda], aux[derecha]):
                arr[k] = aux[izquierda]
                izquierda += 1
            else:
                arr[k] = aux[derecha]
                derecha += 1

    merge_sort_recursive(elementos, auxiliar, 0, tamaño - 1)
    lista["size"] = len(elementos)
    return lista


def quick_sort(lista, sort_criteria=default_sort_criteria):
    
    n = lista["size"]
    if n <= 1:
        return lista  

    elementos = lista["elements"]
    def quick_sort_recursive(elementos, primer_indice, ultimo_indice):
        if primer_indice >= ultimo_indice:
            return  

        elemento_clave = elementos[(primer_indice + ultimo_indice) // 2]

        izquierda = primer_indice  
        i = primer_indice          
        derecha = ultimo_indice    

        while i <= derecha:
            if sort_criteria(elementos[i], elemento_clave) and not sort_criteria(elemento_clave, elementos[i]):
                elementos[izquierda], elementos[i] = elementos[i], elementos[izquierda]
                izquierda += 1
                i += 1
            elif sort_criteria(elemento_clave, elementos[i]) and not sort_criteria(elementos[i], elemento_clave):
                elementos[i], elementos[derecha] = elementos[derecha], elementos[i]
                derecha -= 1
            else:
                i += 1

        quick_sort_recursive(elementos, primer_indice, izquierda - 1)
        quick_sort_recursive(elementos, derecha + 1, ultimo_indice)

    quick_sort_recursive(elementos, 0, n - 1)
    lista["size"] = len(elementos)
    return lista


                    