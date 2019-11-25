from random import randint
from termcolor import colored
from operator import itemgetter


class Matrix:

    def __init__(self, empty_cell_percentage, record_mode, keep_original=False):
        self.num_users = 50
        self.num_items = 20
        self.matrix = [[0 for x in range(self.num_users)]
                       for y in range(self.num_items)]
        self.movies = []
        self.empty_cell_percentage = empty_cell_percentage
        self.record_mode = record_mode
        self.file = "matrix_files/matrix_{}_percent_empty.txt".format(
            empty_cell_percentage)
        self.keep_original = keep_original
        self.__populate()

    def __populate(self):
        # reads directly from the file holding a matrix with the desired percentage of empty cells
        if not self.record_mode:
            self.read(self.file)
            return

        # reads from the fully populated matrix and only then empties some of the cells
        self.read()

        if self.keep_original:
            return

        for i in range(self.num_users):
            for j in range(self.num_items):
                cell_is_empty = randint(0, 100) < self.empty_cell_percentage
                if cell_is_empty:
                    self.matrix[i][j] = 0

        self.persist()

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
        print("Saving to file: %s\n\n" % (self.file))

        f = open(self.file, "w")

        for movie in self.movies:
            f.write("%s\n" % (movie))

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}\t".format(self.matrix[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")

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

        for i in predicted_ratings:
            user, item, predicted_rating = i
            self.matrix[user][item] = colored(
                predicted_rating.rounded, "green")

        for movie in self.movies:
            f.write("%s\n" % (movie))

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}\t".format(self.matrix[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")

    def compare(self, predicted_ratings):
        compare_array = []
        for rating in predicted_ratings:
            user, item, pred_rating = rating
            pred_rating_val = pred_rating.unrounded

            difference_real_predicted = abs(
                self.matrix[user][item] - pred_rating_val)
            compare_array.append((user, item, difference_real_predicted))
        # sort in ascending order of difference_real_predicted
        # (i.e. how good the prediction is)
        return sorted(compare_array, key=itemgetter(2))