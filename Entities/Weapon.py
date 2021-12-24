from random import uniform


class Weapon:

    def __init__(self, name, weight, w_effective_range, w_max_range, effective_range_precision, max_range_precision, damage, damage_area, fire_rate, ammunition_capacity, reliability):
        self.name = name
        self.weight = weight
        self.w_effective_range = w_effective_range
        self.w_max_range = w_max_range
        self.effective_range_precision = effective_range_precision
        self.max_range_precision = max_range_precision
        self.damage = damage
        self.damage_area = damage_area
        self.fire_rate = fire_rate
        self.ammunition_capacity = ammunition_capacity
        self.reliability = reliability

    # Parametros:
    # distance: distancia hacia el objetivo
    # s_precision: precision del soldado
    # visibility_impairment: afectacion de la visibilidad segun el clima
    # target_concealment: ocultamiento del objetivo
    # crit_chance: probabilidad de golpe critico
    # affinity: afinidad del soldado con el arma
    # El metodo fire devuelve el dano realizado por el arma
    def fire(self, distance, s_precision, visibility_impairment, target_concealment, affinity, crit_chance):

        if distance < self.w_effective_range:
            range_precision = self.effective_range_precision
        else:
            if distance < self.w_max_range:
                range_precision = self.max_range_precision
            else:
                range_precision = 0

        hit_chance = affinity*range_precision*s_precision*(1-visibility_impairment)*(1-target_concealment)
        damage = 0
        # Cada disparo capaz de realizar el arma en un turno acierta con la probabilidad: hit_chance
        # Cada disparo tiene una probabilidad (crit_chance) de realizar el doble de dano
        for i in range(self.fire_rate):
            shot = uniform(0, 1)
            if shot <= hit_chance:
                damage += self.damage
                crit = uniform(0, 1)
                if crit <= crit_chance:
                    damage += self.damage

        return damage
