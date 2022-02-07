from Sim.Entities.Terrain import Terrain
from math import inf


class Map:

    def __init__(self, rows, cols):
        self.terrain_matrix = []
        self.restriction_matrix = []
        # Definimos una matriz rows x cols compuesta de Terrains
        for i in range(rows):
            self.terrain_matrix.append([])
            self.restriction_matrix.append([])
            for j in range(cols):
                self.terrain_matrix[i].append(Terrain(''))
                self.restriction_matrix[i].append(1)

    def replace_restrictions(self, restriction_matrix):

        if len(restriction_matrix) == len(self.terrain_matrix):
            if len(restriction_matrix[0]) == len(self.terrain_matrix[0]):
                for i in range(len(restriction_matrix)):
                    for j in range(len(restriction_matrix[0])):
                        self.terrain_matrix[i][j].m_restriction = restriction_matrix[i][j]
                        self.restriction_matrix[i][j] = restriction_matrix[i][j]
                        if restriction_matrix[i][j] == inf:
                            self.terrain_matrix[i][j].available = False

    def add_terrain_matrix(self, terrain_matrix):

        if len(terrain_matrix) == len(self.terrain_matrix):
            if len(terrain_matrix[0]) == len(self.terrain_matrix[0]):
                for i in range(len(terrain_matrix)):
                    for j in range(len(terrain_matrix[0])):
                        self.restriction_matrix[i][j] = terrain_matrix[i][j].m_restriction
                        self.terrain_matrix[i][j] = terrain_matrix[i][j]
                        if terrain_matrix[i][j] == inf:
                            self.terrain_matrix[i][j].available = False


