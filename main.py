# ###########################################################
# ######## Adaptive Systems Project Assignment ##############
# ###########################################################
# Developed by:
#   Daniel Pavez
#   Vicente Canas
# ###########################################################

from matrix import *
from algorithm import *
import sys

# Command line argument crude validation and reading (in order)
if len(sys.argv) < 4:
    print("Incorrect number of arguments, check the Readme file")
    exit()
empty_cell_percentage = int(sys.argv[1])
k_neighbors = int(sys.argv[2])
n_rated_items = int(sys.argv[3])
record_mode = len(sys.argv) == 5 and sys.argv[4] == "--recordMode"

# get original and full matrix to compare with the predicted values
keep_original = True  # prevents matrix from populating with empty cells
original_matrix = Matrix(0, True, keep_original)

# True write in matrix_<empty_cell_percentage>_empty_cells.txt / False read from matrix.txt
gen_matrix = Matrix(empty_cell_percentage, record_mode)
matrix = gen_matrix.matrix

print("%.2f percent of the matrix cells are empty" %
      (gen_matrix.empty_cells_percentage()))

# running k-nearest-neighbors with users
# KNN class instance with the matrix passed as parameter
alg = KNN_users(matrix, k_neighbors, n_rated_items)

# running the algorithm returns the predicted ratings for the entire matrix
# gets the list of top predicted items
predicted_ratings = alg.run()
best_predicted_items = original_matrix.compare(predicted_ratings)[
    0:n_rated_items]
print(best_predicted_items)
# generates a new matrix with the empty cells filled with
# the predicted ratings
# TODO: generate an excel file with this matrix
# currently it is just generating a txt file
gen_matrix.record_predicted(predicted_ratings)
gen_matrix.record_predicted_rounded(predicted_ratings)