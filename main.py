from random import randint

# Constants
num_users = 50
num_items = 20
empty_cell_percentage = 25  # approximate percentage, it is random but based on this

# If set to True, a new matrix will be created and stored in matrix.txt
# If False reads an existing matrix from file (to be able to study the same array in depth)
record_mode = True


def randomCellValue():
    # generates random values taking into account the percentage of
    # empty cells we want to achieve
    cell_is_empty = randint(0, 100) < empty_cell_percentage
    return 0 if cell_is_empty else randint(1, 5)


class Matrix:

    def __init__(self):
        self.matrix = [[0 for x in range(num_users)] for y in range(num_items)]
        self.populate()

    def populate(self):
        if not record_mode:
            self.read()
            return

        for i in range(num_items):
            for j in range(num_users):
                self.matrix[i][j] = randomCellValue()

        self.persist()

    def pretty_print(self):
        for i in range(num_items):
            for j in range(num_users):
                print(self.matrix[i][j] if self.matrix[i]
                      [j] != 0 else "_", end=' ')
                if j == num_users - 1:
                    print("\n")

    def empty_cells_percentage(self):
        counter = 0
        for i in range(num_items):
            for j in range(num_users):
                if self.matrix[i][j] == 0:
                    counter += 1

        return counter * 100 / (num_users * num_items)

    def persist(self):
        f = open("matrix.txt", "w")
        for i in range(num_items):
            for j in range(num_users):
                f.write("{} ".format(self.matrix[i][j]))
                if j == num_users - 1:
                    f.write("\n")

    def read(self):
        self.matrix = []
        f = open("matrix.txt", "r")
        for line in f:
            self.matrix.append(list(map(int, line.split())))


matrix = Matrix()
matrix.pretty_print()

print("%.2f of the matrix cells are empty!" %
      (matrix.empty_cells_percentage()))
