# List Comprehension

# Even numbers from a matrix

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

even_nums = [ n for row in matrix for n in row if n %2 == 0 ]
print(even_nums)


# Flattening a 2D list

matrix = [[1, 2], [3, 4], [5, 6]]

flat = [ num for row in matrix for num in row]
print(flat)







