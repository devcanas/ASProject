from random import randint
from termcolor import colored
from operator import itemgetter
from algorithm import *

class Matrix:

    def __init__(self, empty_cell_percentage, record_mode, keep_original=False):
        self.num_users = 50
        self.num_items = 20
        self.matrix = [[0 for x in range(self.num_users)]
                       for y in range(self.num_items)]
        self.movies = []
        self.empty_cell_percentage = empty_cell_percentage
        self.record_mode = record_mode
        self.file = "matrix_files/matrix_{}_percent_empty".format(
            empty_cell_percentage)
        self.keep_original = keep_original
        self.__populate()

    def __populate(self):
        # reads directly from the file holding a matrix with the desired percentage of empty cells
        if not self.record_mode:
            self.read(self.file + '.txt')
            return

        # reads from the fully populated matrix and only then empties some of the cells
        self.read()

        if self.keep_original:
            return

        counter = 0
        while (True):
            for i in range(self.num_users):
                for j in range(self.num_items):
                    if (counter * 100.0 / (self.num_users * self.num_items) < self.empty_cell_percentage):
                        cell_is_empty = randint(1, 100) == 1
                        if cell_is_empty and self.matrix[i][j] != 0:
                            self.matrix[i][j] = 0
                            counter += 1
                    else:
                        self.persist()
                        self.persist_dataset()
                        return

    def pretty_print(self):
        for i in range(self.num_users):
            for j in range(self.num_items):
                print(self.matrix[i][j] if self.matrix[i][j]
                      != 0 else "__", end='\t')
                if j == self.num_items - 1:
                    print("\n")

    def empty_cells_percentage(self):
        counter = 0
        for i in range(self.num_users):
            for j in range(self.num_items):
                if self.matrix[i][j] == 0:
                    counter += 1

        return counter * 100 / (self.num_users * self.num_items)

    def persist(self):
        print("Saving to file: %s\n\n" % (self.file + ".txt"))

        f = open(self.file + ".txt", "w")

        for movie in self.movies:
            f.write("%s\n" % (movie))

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}\t".format(self.matrix[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")

    def persist_dataset(self):
        f = open(self.file + "_dataset.txt", "w")
        for i in range(self.num_users):
            for j in range(self.num_items):
                if (self.matrix[i][j] != 0):
                    f.write(str(i) + "\t" + str(j) + "\t" + str(self.matrix[i][j]) + "\n")


    def read(self, file="matrix_files/matrix.txt"):
        print("Reading from file: %s\n\n" % (file))

        self.matrix = []
        with open(file) as f:
            lines = f.readlines()

            movies = lines[:self.num_items]
            self.movies = list(map(lambda x: x.strip(), movies))

            ratings = lines[self.num_items:]
            self.matrix = list(
                map(lambda ratings: [float(r) for r in ratings.split()], ratings))

    def record_predicted(self, predicted_ratings):

        f = open("matrix_files/predicted_matrix_{}_percent_empty.txt".format(
            self.empty_cell_percentage), "w")

        matrix_predicted = [row[:] for row in self.matrix]

        for i in predicted_ratings:
            user, item, predicted_rating = i
            matrix_predicted[user][item] = predicted_rating.unrounded

        for movie in self.movies:
            f.write("%s\n" % (movie))

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}\t".format(matrix_predicted[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")

    def record_predicted_rounded(self, predicted_ratings):
        f = open("matrix_files/predicted_matrix_rounded_{}_percent_empty.txt".format(
            self.empty_cell_percentage), "w")

        matrix_predicted = [row[:] for row in self.matrix]

        for i in predicted_ratings:
            user, item, predicted_rating = i
            matrix_predicted[user][item] = predicted_rating.rounded

        for movie in self.movies:
            f.write("%s\n" % (movie))

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}\t".format(matrix_predicted[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")

    def n_top(self, predicted_ratings, n, threshold=4):
        users_recommendations = []

        for i in range(self.num_users):
            user_prs = []
            for p in predicted_ratings:
                user, item, predicted_rating = p
                if (user == i and predicted_rating.unrounded >= threshold):
                    user_prs.append((item, predicted_rating.unrounded))
            users_recommendations.append((i, sorted(user_prs, key=itemgetter(1), reverse=True)[0:n]))

        return users_recommendations

    def n_top_rounded(self, predicted_ratings, n, threshold=4):
        users_recommendations = []

        for i in range(self.num_users):
            user_prs = []
            for p in predicted_ratings:
                user, item, predicted_rating = p
                if (user == i and predicted_rating.rounded >= threshold):
                    user_prs.append((item, predicted_rating.rounded))
            users_recommendations.append((i, sorted(user_prs, key=itemgetter(1), reverse=True)[0:n]))

        return users_recommendations
