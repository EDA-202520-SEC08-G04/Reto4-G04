from ..List import array_list as al
def new_stack():
    return al.new_list()

def push(my_stack,element):
    return al.add_last(my_stack, element)

def pop(my_stack):
    
    try:
        return al.remove_last(my_stack)

    except IndexError:
        raise Exception('EmptyStructureError: stack is empty')
    
def is_empty(my_stack):
    return al.is_empty(my_stack)


def top(my_stack):
    try:
        return al.last_element(my_stack)
    except IndexError:
        raise Exception('EmptyStructureError: stack is empty')

def size(my_stack):
    return al.size(my_stack)
"""
from ..List import double_linked_list as dl

def new_stack():
    return dl.new_list()

def push(lista,element):
    retorno=dl.add_last(lista,element)
    return retorno

def pop(lista):
    if lista["size"]==0:
        raise Exception('EmptyStructureError: stack is empty')
    else:
        retorno=dl.remove_last(lista)
    return retorno

def is_empty(lista):
    retorno=dl.is_empty(lista)
    return retorno

def top(lista):
    if lista["size"]==0:
        raise Exception('EmptyStructureError: stack is empty')
    else:
        retorno=dl.last_element(lista)
    return retorno["info"]

def size(lista):
    retorno=dl.size(lista)
    return retorno
"""