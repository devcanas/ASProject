from random import randint

class Matrix:

    def __init__(self, num_users, num_items, empty_cell_percentage, record_mode):
        self.matrix = [[0 for x in range(num_users)] for y in range(num_items)]
        self.num_users = num_users
        self.num_items = num_items
        self.empty_cell_percentage = empty_cell_percentage
        self.record_mode = record_mode
        self.populate()

    def populate(self):
        if not self.record_mode:
            self.read()
            return

        for i in range(self.num_items):
            for j in range(self.num_users):
                self.matrix[i][j] = self.randomCellValue()

        self.persist()

    def pretty_print(self):
        for i in range(self.num_items):
            for j in range(self.num_users):
                print(self.matrix[i][j] if self.matrix[i]
                      [j] != 0 else "_", end=' ')
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
        f = open("matrix.txt", "w")
        for i in range(self.num_items):
            for j in range(self.num_users):
                f.write("{} ".format(self.matrix[i][j]))
                if j == self.num_users - 1:
                    f.write("\n")

    def read(self):
        self.matrix = []
        f = open("matrix.txt", "r")
        for line in f:
            self.matrix.append(list(map(int, line.split())))

    def randomCellValue(self):
        # generates random values taking into account the percentage of
        # empty cells we want to achieve
        cell_is_empty = randint(0, 100) < self.empty_cell_percentage
        return 0 if cell_is_empty else randint(1, 5)
