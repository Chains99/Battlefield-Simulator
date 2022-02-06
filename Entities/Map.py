from Entities.Terrain import Terrain
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

    def place_soldier(self, soldier, position):

        if self.terrain_matrix[position[0]][position[1]].available:
            self.terrain_matrix[position[0]][position[1]].available = False
            self.terrain_matrix[position[0]][position[1]].occupied_by_soldier = True
            self.terrain_matrix[position[0]][position[1]].standing_soldier = soldier

    def remove_soldier(self, position):
        if self.terrain_matrix[position[0]][position[1]].occupied_by_soldier:
            self.terrain_matrix[position[0]][position[1]].available = True
            self.terrain_matrix[position[0]][position[1]].occupied_by_soldier = False
            self.terrain_matrix[position[0]][position[1]].standing_soldier = None

    def move_soldier(self, current_pos, new_pos, soldier):
        # Remover soldado de la vieja posicion
        self.terrain_matrix[current_pos[0]][current_pos[1]].occupied_by_soldier = False
        self.terrain_matrix[current_pos[0]][current_pos[1]].standing_soldier = None
        self.terrain_matrix[current_pos[0]][current_pos[1]].available = True
        # Colocar soldado en la nueva posicion
        self.terrain_matrix[new_pos[0]][new_pos[1]].occupied_by_soldier = True
        self.terrain_matrix[new_pos[0]][new_pos[1]].standing_soldier = soldier
        self.terrain_matrix[new_pos[0]][new_pos[1]].available = False

