import generator
import algorithm

num_users = int(input("Number of users: "))
num_items = int(input("Number of movies: "))
empty_cell_percentage = int(input("Percentage of empty cells: "))
record_mode = True #True write in matrix.txt / False read from matrix.txt

matrix = generator.Matrix(num_users, num_items, empty_cell_percentage, record_mode)
matrix.pretty_print()

print("%.2f of the matrix cells are empty!" %
      (matrix.empty_cells_percentage()))

alg = algorithm.Algorithm(matrix.matrix)
# PC test
print(alg.PC(0, 4))