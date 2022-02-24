import numpy as np
from itertools import chain
from sim.Entities.Utilities.aabb_segment_box_collision import detect_box_segment_collision


# Parametros:
# point_a: tupla con las coordenadas del punto a
# point_b: tupla con las coordenadas del punto b
# Devuelve un tupla de funciones (x, y)
# funcion x: evalua la funcion con un valor del dominio
# funcion y: evalua la funcion con un valor de la imagen
def make_linear_function(point_a, point_b):

    # Resolvemos un sitema de ecuaciones para hallar la funcion lineal q contenga ambos puntos
    A = np.array([[point_a[0], 1], [point_b[0], 1]])
    B = np.array([point_a[1], point_b[1]])
    S = np.linalg.solve(A, B)

    return lambda x: S[0]*x + S[1], lambda y: (y - S[1])/S[0]


# Parametros:
# point_a: tupla de coordenadas en la matriz
# terrain_map: matriz a la q pertence point_a
# Devuelve un generador de nodos adyacentes a point_a en terrain_map
# Ignorando los nodos a la izquerda, superior izquiera e inferior izquierda
def non_left_adyacent_nodes(point_a, terrain_map):
    top = max(point_a[0] - 1, 0)
    bottom = min(point_a[0] + 1, len(terrain_map) - 1)
    left = point_a[1]
    right = min(point_a[1] + 1, len(terrain_map[0]) - 1)

    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            yield i, j


def detect_collision(node, eval_f):

    grid_x = (node[0], node[0] + 1)
    grid_y = (node[1], node[1] + 1)

    line_x = (eval_f[1](grid_y[0]), eval_f[1](grid_y[1]))

    if grid_x[0] <= line_x[0] <= grid_x[1] or grid_x[0] <= line_x[1] <= grid_x[1] or line_x[0] < grid_x[0] < line_x[1]:
        return True
    return False


# Falta incluir diferencias de alturas
def detect_sight_obstruction(point_a, point_b, node, terrain_map):

    if not (terrain_map[node[0]][node[1]].terrain_object is None):
        return True


def detect_obstruction(point_a, point_b, terrain_map):

    visited = {}

    if point_a[1] > point_b[1]:
        # Hacemos swap entre point_a y point_b
        tmp = point_a
        point_a = point_b
        point_b = tmp

    # Definimos los puntos grid_a y grid_b como el centro de la casilla q pertenecen
    grid_a = (point_a[0] + 0.5, point_a[1] + 0.5)
    grid_b = (point_b[0] + 0.5, point_b[1] + 0.5)
    
    # eval_f = make_linear_function(grid_a, grid_b)

    tmp = point_a

    while tmp != point_b:
        visited[tmp] = True
        for item in non_left_adyacent_nodes(tmp, terrain_map):
            if not (item in visited):
                #if detect_collision(item, eval_f):
                if detect_box_segment_collision((item[0] + 0.5, item[1] + 0.5), (0.5, 0.5), grid_a, grid_b):
                    tmp = item
                    break

        # Comprobamos si existe una obstruccion de vision en point_a
        if detect_sight_obstruction(point_a, point_b, tmp, terrain_map):
            return True

    return False


def north_visible_squares(point, v_range, terrain_map):

    top = min(point[0], v_range)

    for i in range(1, top + 1):
        left = max(point[1] - i, 0)
        right = min(point[1] + i, len(terrain_map[0])-1)
        for j in range(left, right+1):
            yield point[0] - i, j


def south_visible_squares(point, v_range, terrain_map):

    bottom = min(len(terrain_map) - point[0]-1, v_range)

    for i in range(1, bottom + 1):
        left = max(point[1] - i, 0)
        right = min(point[1] + i, len(terrain_map[0])-1)
        for j in range(left, right+1):
            yield point[0] + i, j


def west_visible_squares(point, v_range, terrain_map):

    left = min(point[1], v_range)

    for i in range(1, left + 1):
        top = max(point[0] - i, 0)
        bottom = min(point[0] + i, len(terrain_map)-1)
        for j in range(top, bottom + 1):
            yield j, point[1] - i


def east_visible_squares(point, v_range, terrain_map):

    right = min(len(terrain_map[0]) - point[1]-1, v_range)

    for i in range(1, right + 1):
        top = max(point[0] - i, 0)
        bottom = min(point[0] + i, len(terrain_map)-1)
        for j in range(top, bottom + 1):
            yield j, point[1] + i


def squares_within_range(point, v_range, terrain_map, orientation):

    if orientation == 'north':
        return north_visible_squares(point, v_range, terrain_map)
    if orientation == 'west':
        return west_visible_squares(point, v_range, terrain_map)
    if orientation == 'south':
        return south_visible_squares(point, v_range, terrain_map)
    if orientation == 'east':
        return east_visible_squares(point, v_range, terrain_map)
    # orientation == all
    return chain(north_visible_squares(point, v_range, terrain_map), west_visible_squares(point, v_range, terrain_map), south_visible_squares(point, v_range, terrain_map), east_visible_squares(point, v_range, terrain_map))
