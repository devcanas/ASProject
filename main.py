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

# Get original full matrix to compare with the predicted values
keep_original = True  # prevents matrix from populating with empty cells
original_matrix = Matrix(0, True, keep_original)

# record_mode: True write in matrix_<empty_cell_percentage>_empty_cells.txt / False read from matrix.txt
gen_matrix = Matrix(empty_cell_percentage, record_mode)
matrix = gen_matrix.matrix

print("%.2f percent of the matrix cells are empty" %
    (gen_matrix.empty_cells_percentage()))

# Make the predictions using K-Nearest-Neighbors with users
alg = KNN_users(matrix, k_neighbors)
predicted_ratings = alg.run()

## Save predictions
gen_matrix.record_predicted(predicted_ratings, "knn")
gen_matrix.record_predicted(predicted_ratings, "knn", rounded=True)

## Give the recommendations
gen_matrix.record_n_top(predicted_ratings, n_rated_items, "knn")
gen_matrix.record_n_top(predicted_ratings, n_rated_items, "knn", rounded=True)


# Make the predictions using Singular Value Decomposition (SVD)
rel_path = 'matrix_files/matrix_' + str(empty_cell_percentage) + '_percent_empty_dataset.csv'
svd = SVD_alg(matrix, rel_path)
svd.fit()
predicted_ratings_svd = svd.predict()

## Save predictions
gen_matrix.record_predicted(predicted_ratings_svd, "svd")
gen_matrix.record_predicted(predicted_ratings_svd, "svd", rounded=True)

## Give the recommendations
gen_matrix.record_n_top(predicted_ratings_svd, n_rated_items, "svd")
gen_matrix.record_n_top(predicted_ratings_svd, n_rated_items, "svd", rounded=True)

# Measure quality of predictions (MAE)
print("-----MAE (Mean Absolute Error)-----")
print("MAE KNN: " + str(mae(original_matrix, predicted_ratings)))
print("MAE SVD: " + str(mae(original_matrix, predicted_ratings_svd)))
print("MAE KNN rounded: " + str(mae(original_matrix, predicted_ratings, rounded=True)))
print("MAE SVD rounded: " + str(mae(original_matrix, predicted_ratings_svd, rounded=True)))
print()
# Measure precision and recall
print("-----Precision-----")
print("Precision KNN: " + str(precision(original_matrix, predicted_ratings)))
print("Precision SVD: " + str(precision(original_matrix, predicted_ratings_svd)))
print("Precision KNN rounded: " + str(precision(original_matrix, predicted_ratings, rounded=True)))
print("Precision SVD rounded: " + str(precision(original_matrix, predicted_ratings_svd, rounded=True)))
print()
print("-----Recall-----")
print("Recall KNN: " + str(recall(original_matrix, predicted_ratings)))
print("Recall SVD: " + str(recall(original_matrix, predicted_ratings_svd)))
print("Recall KNN rounded: " + str(recall(original_matrix, predicted_ratings, rounded=True)))
print("Recall SVD rounded: " + str(recall(original_matrix, predicted_ratings_svd, rounded=True)))