from generator import *
from algorithm import *
import sys

empty_cell_percentage = int(sys.argv[1])
# True write in matrix_<empty_cell_percentage>_empty_cells.txt / False read from matrix.txt
record_mode = True \
    if len(sys.argv) == 3 and sys.argv[2] == "--recordMode" \
    else False

generator = Generator(empty_cell_percentage, record_mode)
matrix = generator.matrix
# generator.pretty_print()

print("%.2f percent of the matrix cells are empty" %
      (generator.empty_cells_percentage()))

alg = Algorithm(matrix)

# PC test
# print(alg.pc(0, 4))
# print(alg.pclib(0, 4))
# print(alg.neighbors(0, 2, 5))

predicted_ratings = []
for i in range(len(matrix[0])):
    if matrix[0][i] == 0:
        predicted_ratings.append(
            alg.predicted_rating(0, i, alg.neighbors(0, i, 10)))

print(predicted_ratings)

generator.record_predicted(predicted_ratings)
