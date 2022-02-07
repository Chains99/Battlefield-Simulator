from random import uniform


class Weapon:

    def __init__(self, name, weight, w_effective_range, w_max_range, effective_range_precision, max_range_precision,
                 damage, damage_area, fire_rate, ammunition_capacity, current_ammo, reliability):
        self.name = name
        self.weight = weight
        self.w_effective_range = w_effective_range
        self.w_max_range = w_max_range
        self.effective_range_precision = effective_range_precision
        self.max_range_precision = max_range_precision
        self.damage = damage
        self.fire_rate = fire_rate
        self.ammunition_capacity = ammunition_capacity
        self.current_ammo = current_ammo

    def _average_hit_chance(self, params):
        media = 0
        for item in params:
            media += item
        return media / len(params)

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

        hit_chance = self._average_hit_chance(
            [affinity, range_precision, s_precision, (1 - target_concealment), (1 - visibility_impairment)])
        damage = 0
        # Cada disparo capaz de realizar el arma en un turno acierta con la probabilidad: hit_chance
        # Cada disparo tiene una probabilidad (crit_chance) de realizar el doble de dano
        for i in range(min(self.fire_rate, self.current_ammo)):
            self.current_ammo -= 1
            shot = uniform(0, 1)
            if shot <= hit_chance:
                damage += self.damage
                crit = uniform(0, 1)
                if crit <= crit_chance:
                    damage += self.damage

        return damage

    # Recarga una cantidad de municion: ammo_amount
    def load_ammo(self, ammo_amount):
        if self.current_ammo == self.ammunition_capacity:
            return
        self.current_ammo += ammo_amount


# Definiendo lista de parametros de las armas por defecto
default_weapons = {'Barret': ['Barret', 0.8, 800, 1500, 1, 0.7, 10, 0, 1, 10, 10, 1],  # sniper rifles
                   'AK 47': ['AK 47', 0.8, 300, 1000, 0.7, 0.4, 2, 0, 10, 30, 1],  # assault rifles
                   'M16': ['M16', 0.8, 300, 1000, 0.7, 0.4, 2, 0, 31, 31, 31, 1],
                   'M4': ['M4', 0.8, 300, 1000, 0.7, 0.4, 2, 0, 31, 31, 31, 1],
                   'Scar': ['Scar', 0.8, 300, 1000, 0.7, 0.4, 2, 0, 31, 31, 31, 1],
                   'Mp5': ['Mp5', 0.8, 300, 1000, 0.7, 0.4, 2, 0, 31, 31, 31, 1],  # sub rifle
                   'Beretta M9': ['Beretta M9', 0.2, 50, 100, 0.9, 0.6, 1, 0, 5, 15, 15, 1]}  # handguns
# ( name, weight, w_effective_range, w_max_range, effective_range_precision, max_range_precision, damage, damage_area, fire_rate, ammunition_capacity, reliability)
