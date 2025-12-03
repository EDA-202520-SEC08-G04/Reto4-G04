from ..List import array_list as al
def new_queue():
    return al.new_list()



def enqueue(my_queue, any):
    return al.add_last(my_queue, any)


def dequeue(my_queue):
    try:
        return al.remove_first(my_queue) 
    except IndexError:
        raise Exception("EmptyStructureError: queue is empty")

def is_empty(my_queue):
    return al.is_empty(my_queue)

def peek(my_queue):
    if is_empty(my_queue):
        raise Exception('EmptyStructureError: queue is empty')
    return al.get_element(my_queue,0)

def size(my_queue):
    return al.size(my_queue)
"""
from ..List import double_linked_list as dl

def new_queue():
    return dl.new_list()

def enqueue(my_list,element):
    return dl.add_last(my_list,element)

def dequeue(my_list):
    try:
        return dl.remove_first( my_list)
    except:
        raise Exception("EmptyStructureError: queue is empty")

def is_empty(my_queue):
    return dl.is_empty(my_queue)

def peek(my_list):
    if is_empty(my_list):
        raise Exception('EmptyStructureError: queue is empty')
    elemento=dl.first_element(my_list)
    return elemento["info"]

def size(my_list):
    return dl.size(my_list)
    
"""