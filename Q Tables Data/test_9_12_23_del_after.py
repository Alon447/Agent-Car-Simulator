import pickle
import numpy
import heapq

def find_top_values_2d_array(matrix, n=10):
    if not matrix or not matrix[0]:
        return None  # Empty matrix

    flat_matrix = [element for row in matrix for element in row]
    top_values = heapq.nlargest(n, flat_matrix)

    return top_values

# Example usage:

def find_top_values_and_indexes_2d_array(matrix, n=10):
    if not matrix or not matrix[0]:
        return None  # Empty matrix

    flat_matrix = [(element, (i, j)) for i, row in enumerate(matrix) for j, element in enumerate(row)]
    top_values_with_indexes = heapq.nlargest(n, flat_matrix, key=lambda x: x[0])

    return top_values_with_indexes


def find_max_2d_array(matrix):
    if not matrix or not matrix[0]:
        return None  # Empty matrix

    max_value = matrix[0][0]

    for row in matrix:
        for element in row:
            if element > max_value:
                max_value = element

    return max_value

with open('q_table_TLV_659_668_evening_5.pkl', 'rb') as f:
    q_table = pickle.load(f)
    top_values_with_indexes = find_top_values_and_indexes_2d_array(q_table, 100)
    print("Top 10 values with indexes:")
    for value, indexes in top_values_with_indexes:
        print(f"Value: {value}, Indexes: {indexes}")