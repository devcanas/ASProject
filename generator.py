from random import randint


class Matrix:

    def __init__(self, empty_cell_percentage, record_mode):
        self.num_users = 50
        self.num_items = 20
        self.matrix = [[0 for x in range(self.num_users)]
                       for y in range(self.num_items)]
        self.empty_cell_percentage = empty_cell_percentage
        self.record_mode = record_mode
        self.file = "matrix_files/matrix_{}_percent_empty.txt".format(
            empty_cell_percentage)
        self.populate()

    def populate(self):
        # reads directly from the file holding a matrix of self.empty_cell_percentage empty cells
        if not self.record_mode:
            self.read(self.file)
            return

        # reads from the fully populated matrix and only then empties some of the cells
        self.read()
        for i in range(self.num_items):
            for j in range(self.num_users):
                cell_is_empty = randint(0, 100) < self.empty_cell_percentage
                if cell_is_empty:
                    self.matrix[i][j] = 0

        self.persist()

    def pretty_print(self):
        for i in range(self.num_items):
            for j in range(self.num_users):
                print(self.matrix[i][j] if self.matrix[i]
                      [j] != 0.0 else self.matrix[i][j], end='\t')
                if j == self.num_users - 1:
                    print("\n")

    def empty_cells_percentage(self):
        counter = 0
        for i in range(self.num_items):
            for j in range(self.num_users):
                if self.matrix[i][j] == 0:
                    counter += 1

        return counter * 100 / (self.num_users * self.num_items)

    def persist(self):
        f = open(self.file, "w")
        for i in range(self.num_items):
            for j in range(self.num_users):
                f.write("{}\t".format(self.matrix[i][j]))
                if j == self.num_users - 1:
                    f.write("\n")

    def read(self, file="matrix_files/matrix.txt"):
        self.matrix = []
        f = open(file, "r")
        for line in f:
            self.matrix.append(list(map(float, line.split())))
