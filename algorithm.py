from math import pow, sqrt

class Algorithm:

    def __init__(self, matrix):
        self.matrix = matrix

    # Calculate the PC between 2 users, given their index in the matrix (u and v)
    def pc(self, u, v):
        n_items = len(self.matrix)
        n_users = len(self.matrix[0])

        # Ratings of items rated by both users
        ratings_u = []
        ratings_v = []
        for i in range(n_items):
            ru = self.matrix[i][u]
            rv = self.matrix[i][v]
            
            if (ru != 0 and rv != 0):
                ratings_u.append(ru)
                ratings_v.append(rv)
        
        # Mean of ratings given by user u (items rated by both users)
        mean_u = 0
        for i in ratings_u:
            mean_u += i
        mean_u /= len(ratings_u)

        # Mean of ratings given by user v (items rated by both users)
        mean_v = 0
        for i in ratings_v:
            mean_v += i
        mean_v /= len(ratings_v)

        # Calculation of PC
        up = 0
        for i in range(len(ratings_u)):
            up += (ratings_u[i] - mean_u) * (ratings_v[i] - mean_v)
        
        down1 = 0
        for ru in ratings_u:
            v = (ru - mean_u)
            down1 += pow(v, 2)

        down2 = 0
        for rv in ratings_v:
            v = (rv - mean_v)
            down2 += pow(v, 2)

        down = sqrt(down1 * down2)

        # If the denominator is 0, return 1 (higher value of PC)
        return 1 if down == 0 else up/down

    #def predicted_rating(self, u, v):
    #    w = self.pc(u,v)

