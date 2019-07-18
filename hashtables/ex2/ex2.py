#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """
    for ticket in tickets:
        hash_table_insert(hashtable, str(ticket.source), str(ticket.destination))
    start_key = "NONE"
    start_value = hash_table_retrieve(hashtable, start_key)
    route[0] = start_value
    index = 1
    while start_value != "NONE":
        start_key = start_value
        start_value = hash_table_retrieve(hashtable, start_key)
        if start_value is not None: 
            route[index] = start_value
            index += 1
    return route
