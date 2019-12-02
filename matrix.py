from random import randint
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
            self.read()
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
        f = open(self.file + ".csv", "w")

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{}".format(self.matrix[i][j]))
                if j == self.num_items - 1:
                    f.write("\n")
                else:
                    f.write(";")

    def persist_dataset(self):
        f = open(self.file + "_dataset.csv", "w")
        for i in range(self.num_users):
            for j in range(self.num_items):
                if (self.matrix[i][j] != 0):
                    f.write(str(i) + ";" + str(j) + ";" + str(self.matrix[i][j]) + "\n")


    def read(self):
        file="matrix_files/matrix.txt"

        with open(file) as f:
            lines = f.readlines()

            movies = lines[:self.num_items]
            self.movies = list(map(lambda x: x.strip(), movies))

        if(self.record_mode == False):
            file = self.file + ".csv"

        self.matrix = []

        with open(file) as f:
            lines = f.readlines()
            ratings = lines
            separator = ';'
            if(self.record_mode):
                ratings = ratings[self.num_items:]
                separator = ' '
            self.matrix = list(
                map(lambda ratings: [float(r) for r in ratings.split(separator)], ratings))

    def record_predicted(self, predicted_ratings, alg, rounded=False):
        file = "matrix_files/{}_predicted_matrix_{}_percent_empty.csv".format(alg, self.empty_cell_percentage)

        if(rounded):
            file = "matrix_files/{}_predicted_matrix_rounded_{}_percent_empty.csv".format(alg, self.empty_cell_percentage)
            
        f = open(file, "w")

        matrix_predicted = [row[:] for row in self.matrix]

        for i in predicted_ratings:
            user, item, predicted_rating = i
            p_rating = predicted_rating.unrounded
            if(rounded):
                p_rating = predicted_rating.rounded
            matrix_predicted[user][item] = p_rating

        for movie in self.movies:
            f.write("%s;" % (movie))
        f.write("\n")

        for i in range(self.num_users):
            for j in range(self.num_items):
                f.write("{};".format(matrix_predicted[i][j]).replace('.',','))
                if j == self.num_items - 1:
                    f.write("\n")

    def record_n_top(self, predicted_ratings, n, alg, rounded=False, threshold=4):
        users_recommendations = []
        users_filtered_recommendations = []
        for i in range(self.num_users):
            user_prs = []
            for p in predicted_ratings:
                user, item, predicted_rating = p
                p_rating = predicted_rating.unrounded
                if(rounded):
                    p_rating = predicted_rating.rounded
                if (user == i and p_rating >= threshold):
                    user_prs.append((item, p_rating))
            users_recommendations.append((i, sorted(user_prs, key=itemgetter(1), reverse=True)[0:n]))
            for u in user_prs:
                users_filtered_recommendations.append(u)

        # Record
        file = "matrix_files/{}_n_top_{}_percent_empty.csv".format(alg, self.empty_cell_percentage)

        if(rounded):
            file = "matrix_files/{}_n_top_{}_percent_empty.csv".format(alg, self.empty_cell_percentage)

        f = open(file, "w")

        f.write("User ID;")
        for i in range(n):
            f.write("Recommendation {};".format(i))
        f.write("\n")

        for user_recommendations in users_recommendations:
            user, recommendations = user_recommendations
            f.write(str(user + 1))
            for recommendation in recommendations:
                movie_id, rating = recommendation
                f.write(";Movie ID: {} / Movie: {} / Predicted rating: {}".format(str(movie_id + 1), self.movies[movie_id], str(rating).replace('.',',')))
            f.write("\n")
        return users_filtered_recommendations
