from A_star.A_star import a_star
from A_star.A_star import euclidean_distance
from Entities.Utilities import Sight


class Soldier:

    def __init__(self, id, health, vision_range, precision, move_speed, crit_chance, orientation, stance, max_load, concealment, team):
        self.id = id
        self.health = health
        self.vision_range = vision_range
        self.precision = precision
        self. move_speed = move_speed
        self.crit_chance = crit_chance
        # diccionario nombre: valor
        self.w_affinities = {}
        self.orientation = orientation
        self.stance = stance
        self.max_load = max_load
        self.concealment = concealment
        self.team = team
        self.equipped_weapon = None
        self.weapons = []

    # Parametros:
    # position: posicion inicial del soldado
    # speed: velocidad del soldado
    # restriction map: mapa
    # El metodo devuelve la maxima casilla alcanzable con el valor de speed, en el camino optimo de position a destiny
    # Falta la orientacion al caminar
    def move_to(self, position, destiny, restriction_map, terrain_map):

        speed = self.move_speed

        # Hallamos el camino optimo de position a destiny
        path = a_star(restriction_map, lambda x: euclidean_distance(x, destiny), position, destiny, terrain_map)
        # Si no existe un camino hasta destiny no se mueve
        if path is None:
            return position
        # Cada casilla que se avanza resta speed al soldado, con 0 speed no puede avanzar mas
        for item in path:
            if speed < 0:
                return position
            position = item
            speed -= restriction_map[item[0]][item[1]]

        return position

    def detect_enemies(self, pos, terrain_map):

        # Encontramos todas las casillas en el rango de vision
        squares = Sight.squares_within_range(pos, self.vision_range, terrain_map, 'all')
        enemies = []
        # Encontramos si existen soldados enemigos en el rango de vision
        for item in squares:
            if terrain_map[item[0]][item[1]].occupied_by_soldier:
                # Si el soldado no es del mismo equipo es enemigo
                if self.team != terrain_map[item[0]][item[1]].standing_soldier.team:
                    if not Sight.detect_obstruction(pos, item, terrain_map):
                        enemies.append(item)

        return enemies

    def shoot(self, distance, visibility, target_concealment):
        aff = 1
        if self.equipped_weapon.name in self.w_affinities.keys():
            aff = self.w_affinities[self.equipped_weapon.name]

        damage = self.equipped_weapon.fire(distance, self.precision, visibility, target_concealment, aff, self.crit_chance)
        return damage

