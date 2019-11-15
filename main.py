import generator
import algorithm
import sys

empty_cell_percentage = int(sys.argv[1])
# True write in matrix_<empty_cell_percentage>_empty_cells.txt / False read from matrix.txt
record_mode = bool(sys.argv[2])

matrix = generator.Matrix(empty_cell_percentage, record_mode)
matrix.pretty_print()

print("%.2f of the matrix cells are empty!" %
      (matrix.empty_cells_percentage()))

alg = algorithm.Algorithm(matrix.matrix)
# PC test
print(alg.pc(0, 4))
