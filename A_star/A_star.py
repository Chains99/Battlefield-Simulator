from queue import PriorityQueue
from A_star.heap import node_heap,heapify_down,heapify_up,extract_min,append_node
from math import inf
from math import pow


# Recibe x, y componentes de la matriz y devuelve la distancia euclideana entre ellos
def euclidean_distance(x, y):

    distance = pow(x[0] - y[0], 2) + pow(x[1] - y[1], 2)
    distance = pow(distance, 0.5)

    return distance


# Construimos un heap con los nodos del mapa con un valor inicial inf
def init_nodes(map):

    nodes = []

    for i in range(len(map)):
        for j in range(len(map[0])):
            nodes.append(node_heap((i, j), inf, inf))
            # definidos el id del nodo como una tupla (i, j) con la fila y columna del nodo
    return nodes


# Actualizamos el peso/costo de cada nodo con el valor de la heuristica
def make_hw_map(map, hs):

    for i in range(len(map)):
        for j in range(len(map[0])):
            map[i][j] = (map[i][j] + hs((i, j)))

    return map


# Genera los nodos adyacentes al nodo en la posicion pos en la matriz map
def adyacent_nodes(map, pos):

    top = max(pos[0]-1, 0)
    bottom = min(pos[0]+1, len(map)-1)
    left = max(pos[1]-1, 0)
    right = min(pos[1] + 1, len(map[0])-1)

    for i in range(top, bottom+1):
        for j in range(left, right+1):
            yield (i, j)


# Creamos un camino directo desde s hasta d, creado con cada componente del camino
# Devuelve None si no existe un camino
def make_path(path, s, d, cols):

    #Si no existe camino
    if path[d[0] * cols + d[1]] == inf:
        return None
    direct_path = []
    titem = d
    while titem != s:
        direct_path.append(titem)
        titem = path[titem[0] * cols + titem[1]]
    direct_path.append(titem)

    # Devolvemos un generador con el orden invertido al de direct_path
    for i in range(len(direct_path)):
        yield direct_path[len(direct_path)-1-i]

"""
Hs funcion lambda : lambda x -> y
Donde y es el valor de la heuristica asociado a x
"""

"""
a_star(matriz, hs, s, d)
parametros:
matriz: matriz con los valores de consumo de movimiento de cada casilla (costo),
si una casilla no puede ser transitada toma valor inf
hs funcion lambda : lambda x -> y donde y es el valor de la heuristica asociado a x
s: nodo inicial (i,j) fila i columna j
d: nodo destino (i,j)

Algoritmo de A-star para encontrar encontrar el camino mas corto de un punto de una matriz a otro
Devuelve una lista tupla (i,j) que representa el camino optimo de s a d
"""


def a_star(map, hs, s, d, terrain_map):

    visited = []
    for i in range(len(map)):
        visited.append([False]*len(map[0]))

    nodes = init_nodes(map)
    # initialize the heap with the starting node
    heap = []
    # s_pos: la posicion de s en el heap de nodos
    s_pos = s[0]*len(map[0]) + s[1]
    nodes[s_pos].value = 0
    append_node(heap, nodes[s_pos])
    # initialize path list
    path = [inf]*len(nodes)

    path = dijkstra(map, nodes, heap, visited, path, d, hs, terrain_map)
    return make_path(path, s, d, len(map[0]))


def dijkstra(w_graph, nodes, heap, visited, path, destiny, hs, terrain_map):

    while len(heap) > 0:
        u = extract_min(heap)
        visited[u.id[0]][u.id[1]] = True
        if u.id == destiny:
            return path

        for item in adyacent_nodes(w_graph, u.id):
            # Sea item la tupla (i, j) correspondiente a un elemento de w_graph
            # si el elemento en la posicion correspondiente a (i, j) en la lista de nodos tiene valor inf
            if not w_graph[item[0]][item[1]] == inf and terrain_map[item[0]][item[1]].available:
                if not visited[item[0]][item[1]]:
                    if nodes[item[0]*len(w_graph[0]) + item[1]].value == inf:
                        append_node(heap, nodes[item[0]*len(w_graph[0]) + item[1]])
                    relax(u.id, item, w_graph, nodes, heap, path, hs)
    return path


def relax(u, v, graph, nodes, heap, path, hs):

    if nodes[v[0]*len(graph[0])+v[1]].value > nodes[u[0]*len(graph[0])+u[1]].value + graph[v[0]][v[1]] + hs((v[0], v[1])):
        nodes[v[0]*len(graph[0])+v[1]].value = nodes[u[0]*len(graph[0])+u[1]].value + graph[v[0]][v[1]] + hs((v[0], v[1]))
        path[v[0]*len(graph[0])+v[1]] = u
        # Update position in heap
        heapify_up(heap, nodes[v[0]*len(graph[0])+v[1]])




