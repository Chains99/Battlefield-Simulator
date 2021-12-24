from Entities.Terrain import Terrain


def hear_soldiers(point, h_range, terrain_map):

    top = max(point[0] - h_range, 0)
    bottom = min(point[0] + h_range, len(terrain_map) - 1)
    left = max(point[1] - h_range, 0)
    right = min(point[1] + h_range, len(terrain_map[0]) - 1)

    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            if terrain_map[i][j].occupied_by_soldier:
                yield i, j
