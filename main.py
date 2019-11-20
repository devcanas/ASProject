from generator import *
from algorithm import *
import sys

empty_cell_percentage = int(sys.argv[1])
# True write in matrix_<empty_cell_percentage>_empty_cells.txt / False read from matrix.txt
record_mode = True if len(
    sys.argv) == 3 and sys.argv[2] == "--recordMode" else False

matrix = Matrix(empty_cell_percentage, record_mode)
# matrix.pretty_print()

print("%.2f percent of the matrix cells are empty" %
      (matrix.empty_cells_percentage()))

alg = Algorithm(matrix.matrix)
# PC test
print(alg.pc(0, 4))
