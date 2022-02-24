from sim.A_star.A_star import a_star
from sim.A_star.A_star import euclidean_distance
from sim.Entities.Utilities import Sight


class Soldier:

    id = 0

    def __init__(self, health, vision_range, precision, move_speed, crit_chance, orientation, stance, max_load,
                 concealment, team):
        self.id = Soldier.id
        Soldier.id += 1
        self.health = health
        self.current_health = health
        self.vision_range = vision_range

        self.precision = precision
        self.stances_precision = {'standing': precision, 'crouching': min(precision * 1.05, 0.95), 'lying': min(precision * 1.1, 0.95)}

        self.move_speed = move_speed
        self.crit_chance = crit_chance
        # diccionario nombre: valor
        self.w_affinities = {}
        self.orientation = orientation
        self.stance = stance
        self.max_load = max_load

        self.concealment = concealment
        self.stances_concealment = {'standing': concealment, 'crouching': min(concealment * 1.1, 0.95), 'lying': min(concealment * 1.1, 0.95)}
        self.next_to_object = False

        self.team = team
        self.equipped_weapon = None
        self.weapons = []
        # dictionary weapon name: remaining ammo
        self.weapon_ammo = {}

    def detect_object_next(self, position, terrain_map):
        squares = Sight.squares_within_range(position, 1, terrain_map, 'all')
        for item in squares:
            if terrain_map[item[0]][item[1]].terrain_object is not None:
                self.next_to_object = True
                self.concealment = min(self.stances_concealment[self.stance] * 1.3, 0.95)


    # Parametros:
    # position: posicion inicial del soldado
    # speed: velocidad del soldado
    # restriction map: mapa
    # El metodo devuelve la maxima casilla alcanzable con el valor de speed, en el camino optimo de position a destiny
    # Falta la orientacion al caminar
    def move_to(self, position, destiny, restriction_map, terrain_map, soldiers_positions_matrix):

        if self.stance == 'lying':
            return

        self.concealment = self.stances_concealment['standing']
        self.precision = self.stances_precision['standing']
        self.next_to_object = False
        self.stance = 'standing'

        speed = self.move_speed

        # Hallamos el camino optimo de position a destiny
        path = a_star(restriction_map, lambda x: euclidean_distance(x, destiny), position, destiny, terrain_map, soldiers_positions_matrix)
        # Si no existe un camino hasta destiny no se mueve
        if path is None:
            return position
        # Cada casilla que se avanza resta speed al soldado, con 0 speed no puede avanzar mas
        for item in path:
            if speed < 0:
                return position
            position = item
            speed -= restriction_map[item[0]][item[1]]

        self.detect_object_next(position, terrain_map)
        return position

    # Parametros:
    # pos: posicion central del campo de vision
    # terrain_map: matriz de terrenos
    # Devuelve una lista de enemigos en el rango de vision
    def detect_enemies(self, position, terrain_map, reverse_sol_pos):

        # Encontramos todas las casillas en el rango de vision
        squares = Sight.squares_within_range(position, self.vision_range, terrain_map, 'all')
        enemies = []
        # Encontramos si existen soldados enemigos en el rango de vision
        sol_pos = [*reverse_sol_pos.keys()]
        for item in squares:
            # Si en esa posicion hay un soldado
            if item in sol_pos:
                # Si el soldado no es del mismo equipo es enemigo
                if self.team != reverse_sol_pos[item].team:
                    if not Sight.detect_obstruction(position, item, terrain_map):
                        enemies.append(item)

        return enemies

    # Parametros:
    # pos: posicion central del campo de vision
    # terrain_map: matriz de terrenos
    # Devuelve una lista de aliados en el rango de vision
    def detect_allies(self, position, terrain_map, reverse_sol_pos):

        # Encontramos todas las casillas en el rango de vision
        squares = Sight.squares_within_range(position, self.vision_range, terrain_map, 'all')
        enemies = []

        # Encontramos si existen soldados enemigos en el rango de vision
        sol_pos = [*reverse_sol_pos.keys()]
        for item in squares:
            if item in sol_pos:
                # Si el soldado no es del mismo equipo es enemigo
                if self.team == reverse_sol_pos[item].team:
                    if not Sight.detect_obstruction(position, item, terrain_map):
                        enemies.append(item)

        return enemies

    def detect_object(self, position, terrain_map):

        # Encontramos todas las casillas en el rango de vision
        squares = Sight.squares_within_range(position, self.vision_range, terrain_map, 'all')
        objects = []
        # Encontramos si existen objetos enemigos en el rango de vision
        for item in squares:
            if terrain_map[item[0]][item[1]].terrain_object is not None:

                # Si la vision del objeto no esta obstruida
                if not Sight.detect_obstruction(position, item, terrain_map):
                    objects.append(item)
        return objects

    # Parametros:
    # distance: distancia entre el soldado y el objetivo
    # visibility:
    # target_concealment: 
    def shoot(self, distance, visibility, target_concealment):
        aff = 1
        if self.equipped_weapon.name in self.w_affinities.keys():
            aff = self.w_affinities[self.equipped_weapon.name]

        damage = self.equipped_weapon.fire(distance, self.precision, visibility, target_concealment, aff,
                                           self.crit_chance)

        return damage

    def take_damage(self, damage):
        self.current_health -= damage

    def reload(self):
        ammo = self.weapon_ammo[self.equipped_weapon.name]
        to_reload = self.equipped_weapon.ammunition_capacity - self.equipped_weapon.current_ammo
        to_reload = min(ammo, to_reload)
        self.weapon_ammo[self.equipped_weapon.name] -= to_reload
        self.equipped_weapon.load_ammo(to_reload)

    def change_stance(self, stance, position, terrain_map):
        if stance == self.stance:
            return
        self.stance = stance
        self.precision = self.stances_precision[stance]
        self.concealment = self.stances_concealment[stance]
        self.detect_object_next(position, terrain_map)

    def change_weapon(self, weapon_name):

        for item in self.weapons:
            if self.equipped_weapon.name == item.name:
                self.equipped_weapon = item
                break
