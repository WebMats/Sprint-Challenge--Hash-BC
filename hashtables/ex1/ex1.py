#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    answer = None
    for index in range(len(weights)):
        hash_table_insert(ht, weights[index], index)
    for index in range(len(weights)):
        wanted_key = limit - weights[index]
        answer = hash_table_retrieve(ht, wanted_key)
        if answer:
            return (answer, index)
    return answer


def print_answer(answer):
    if answer is None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
