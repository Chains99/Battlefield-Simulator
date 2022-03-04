from Sim.A_star.A_star import euclidean_distance
from Sim.Entities.Soldier import Soldier


def soldier_pos_matrix(sim_map, state):
    rows = len(sim_map.terrain_matrix)
    cols = len(sim_map.terrain_matrix[0])

    soldier_pos_mat = []
    for i in range(rows):
        soldier_pos_mat.append([])
        for j in range(cols):
            soldier_pos_mat[i].append(False)

    sold = [*state.soldier_positions.values()]

    for pos in sold:
        soldier_pos_mat[pos[0]][pos[1]] = True
    return soldier_pos_mat

def new_changed_tuple(tuple_to_change, index_changes_list):
    tuple_list = list(tuple_to_change)
    for item in index_changes_list:
        tuple_list[item[0]] = item[1]
    return tuple(tuple_list)



class ActionManager:

    def __init__(self, weather, sim_map):
        self.weather = weather
        self.map = sim_map
    """
    Soldier actions
    """


    def melee_attack(self, soldier, enemy_pos, state):
        result_state = state.copy_state()
        enemy = state.reverse_soldier_positions[enemy_pos]

        damage = soldier.melee_damage

        # NEW STATE
        change_en = [(10, state.soldier_variables[enemy.id][10] - damage)]
        en_tuple = new_changed_tuple(state.soldier_variables[enemy.id], change_en)
        result_state.soldier_variables[enemy.id] = en_tuple

        if state.soldier_variables[enemy.id][10] - damage <= 0:
            result_state.alive_soldiers[enemy.team] -= 1
            result_state.soldier_died[enemy.team][enemy.id] = True

        return result_state

    def shoot_enemy(self, soldier, enemy_pos, state):
        result_state = state.copy_state()

        pos1 = state.soldier_positions[soldier.id]
        enemy = state.reverse_soldier_positions[enemy_pos]

        # PRE SIMULATION
        current_ammo_in_instance = soldier.equipped_weapon.current_ammo
        current_ammo_in_state = state.soldier_variables[soldier.id][5]
        inst_weapon = soldier.equipped_weapon
        st_weapon = inst_weapon
        st_weapon_name = state.soldier_str_variables[soldier.id][2]

        # If current equipped weapon is different
        if st_weapon_name != soldier.equipped_weapon.name:
            new_weapon_state = self.change_weapon(soldier, st_weapon_name, state)
            current_ammo_in_state = new_weapon_state.soldier_variables[soldier.id][5]
            for wp in soldier.weapons:
                if wp.name == st_weapon_name:
                    current_ammo_in_instance = wp.current_ammo
                    soldier.equipped_weapon = wp
                    st_weapon = wp
                    break

        # SET STATE VALUES
        soldier.equipped_weapon.current_ammo = current_ammo_in_state

        # SIMULATE SHOT
        terrain_camouflage = self.map.terrain_matrix[enemy_pos[0]][enemy_pos[1]].camouflage
        damage, shots_landed = soldier.shoot(euclidean_distance(pos1, enemy_pos), self.weather.visibility_impairment, min(state.soldier_variables[enemy.id][9] * terrain_camouflage, 0.95))

        # REVERT CHANGES
        soldier.equipped_weapon.current_ammo = current_ammo_in_instance
        soldier.equipped_weapon = inst_weapon

        new_current_ammo = current_ammo_in_state - min(current_ammo_in_state, state.soldier_variables[soldier.id][4])

        # NEW STATE
        change_en = [(10, state.soldier_variables[enemy.id][10] - damage)]
        change_sol = [(5, new_current_ammo)]

        sol_tuple = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        en_tuple = new_changed_tuple(state.soldier_variables[enemy.id], change_en)

        result_state.soldier_variables[soldier.id] = sol_tuple
        result_state.soldier_variables[enemy.id] = en_tuple
        result_state.soldier_weapons_current_ammo[soldier.id][state.soldier_str_variables[soldier.id][2]] = new_current_ammo

        if state.soldier_variables[enemy.id][10] - damage <= 0:
            result_state.alive_soldiers[enemy.team] -= 1
            result_state.soldier_died[enemy.team][enemy.id] = True

        return result_state

    def move(self, soldier, position, state):

        if state.soldier_str_variables[soldier.id][0] == 'lying':
            return state

        result_state = state.copy_state()
        sol_position = state.soldier_positions[soldier.id]
        pos_matrix = soldier_pos_matrix(self.map, state)

        # PRE SIMULATION INSTANCE VALUES
        position_instance = soldier.position
        next_object_instance = soldier.next_to_object
        concealment_instance = soldier.concealment
        precision_instance = soldier.precision
        stance_instance = soldier.stance

        # STATE VALUES
        st_stance = state.soldier_str_variables[soldier.id][0]

        # SIMULATE MOVEMENT
        soldier.change_stance(st_stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)
        new_pos = soldier.move_to(sol_position, position, self.map.restriction_matrix, self.map.terrain_matrix, pos_matrix)

        new_concealment = soldier.concealment
        new_precision = soldier.precision
        new_next_object = soldier.next_to_object
        new_stance = soldier.stance

        # REVERT CHANGES
        soldier.position = position_instance
        soldier.concealment = concealment_instance
        soldier.precision = precision_instance
        soldier.stance = stance_instance
        soldier.next_to_object = next_object_instance

        # NEW STATE
        enemies_in_sight, enemies_in_eff_range, allies_in_eff_range, enemies_in_max_range = self._detect_allies_enemies(soldier, result_state)

        change_sol = [(0, enemies_in_sight), (1, allies_in_eff_range), (2, enemies_in_eff_range), (3, enemies_in_max_range), (9, new_concealment), (11, new_precision)]
        change_str_sol = [(0, new_stance), (1, new_next_object)]
        result_state.reverse_soldier_positions.pop(sol_position)

        result_state.soldier_positions[soldier.id] = new_pos
        result_state.reverse_soldier_positions[new_pos] = soldier
        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id], change_str_sol)

        return result_state

    def _detect_allies_enemies(self, soldier, state):
        soldier_pos = state.soldier_positions[soldier.id]
        enemies_in_sight = self.detect_enemies(soldier, state)
        allies_in_sight = self.detect_allies(soldier, state)

        total_en_s = len(enemies_in_sight)
        total_all_r = 0
        total_en_r = 0

        weapon_eff_range = 0
        weapon_name = state.soldier_str_variables[soldier.id][2]

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range

        for enemy_pos in enemies_in_sight:
            if euclidean_distance(soldier_pos, enemy_pos) <= weapon_eff_range:
                total_en_r += 1

        for ally_pos in allies_in_sight:
            if euclidean_distance(soldier_pos, ally_pos) <= weapon_eff_range:
                total_all_r += 1

        total_en_max_r = self.amount_enemies_out_of_effective_range(soldier, enemies_in_sight, state)

        return total_en_s, total_en_r, total_all_r, total_en_max_r

    def change_stance(self, soldier, stance, state):

        result_state = state.copy_state()

        # PRE SIMULATION INSTANCE VALUES
        old_concealment = soldier.concealment
        old_precision = soldier.precision
        old_stance = soldier.stance
        old_next = soldier.next_to_object

        # STATE VALUE
        st_stance = state.soldier_str_variables[soldier.id][0]

        # SIMULATE ACTION
        soldier.change_stance(st_stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)
        soldier.change_stance(stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)

        new_conceal = soldier.concealment
        new_precision = soldier.precision
        new_stance = soldier.stance
        new_next = soldier.next_to_object

        # REVERT CHANGES
        soldier.concealment = old_concealment
        soldier.precision = old_precision
        soldier.stance = old_stance
        soldier.next_to_object = old_next

        # NEW STATE
        change_sol = [(9, new_conceal), (11, new_precision)]
        change__str_sol = [(0, new_stance), (1, new_next)]

        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id], change__str_sol)

        #result_state.soldier_moved[soldier.team][soldier.id] = True
        #result_state.team_variables_moved[soldier.team] += 1

        return result_state

    def reload(self, soldier, state):

        result_state = state.copy_state()

        # PRE SIMULATION VALUES
        weapon_name = state.soldier_str_variables[soldier.id][2]
        current_ammo = state.soldier_variables[soldier.id][5]
        max_ammo = state.soldier_variables[soldier.id][6]
        weapon_ammo = state.soldier_ammo_per_weapon[soldier.id][weapon_name]

        # SIMULATE ACTION
        to_reload = min(weapon_ammo, max_ammo-current_ammo)

        new_current_ammo = current_ammo + to_reload
        new_weapon_ammo = weapon_ammo - to_reload

        # NEW STATE
        change_sol = [(5, new_current_ammo)]

        result_state.soldier_weapons_current_ammo[soldier.id][weapon_name] = new_current_ammo
        result_state.soldier_ammo_per_weapon[soldier.id][weapon_name] = new_weapon_ammo
        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)

        #result_state.soldier_moved[soldier.team][soldier.id] = True
        #result_state.team_variables_moved[soldier.team] += 1

        return result_state

    def change_weapon(self, soldier, weapon_name, state):

        result_state = state.copy_state()

        # NEW STATE
        # damage_ef, damage_nef, fire_rate, current_ammo, ef_ran, nef_ran, ammo_cap
        new_variables = self.change_weapon_variables(soldier, state)

        position = state.soldier_positions[soldier.id]
        enemies_pos = soldier.detect_enemies(position, self.map.terrain_matrix, state)
        count_er = 0
        count_ner = 0
        for enemy_pos in enemies_pos:
            if euclidean_distance(position, enemy_pos) <= new_variables[4]:
                count_er += 1
                continue
            if euclidean_distance(position, enemy_pos) <= new_variables[5]:
                count_ner += 1

        change_sol = [(2, count_er),
                      (3, count_ner),
                      (4, new_variables[2]),
                      (5, new_variables[3]),
                      (6, new_variables[6]),
                      (7, new_variables[1]),
                      (8, new_variables[2])]

        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id], [(2, weapon_name)])
        result_state.soldier_weapons_current_ammo[soldier.id][weapon_name] = new_variables[3]

        #result_state.soldier_moved[soldier.team][soldier.id] = True
        #result_state.team_variables_moved[soldier.team] += 1

        return result_state

    """
    Soldier information
    """
    def detect_enemies(self, soldier, state):
        return soldier.detect_enemies(state.soldier_positions[soldier.id], self.map.terrain_matrix, state)

    def detect_allies(self, soldier, state):
        return soldier.detect_allies(state.soldier_positions[soldier.id], self.map.terrain_matrix, state.reverse_soldier_positions)

    def amount_enemies_in_effective_range(self, soldier, enemies_pos, state):
        count = 0
        soldier_position = state.soldier_positions[soldier.id]

        weapon_eff_range = 0
        weapon_name = state.soldier_str_variables[soldier.id][2]

        if weapon_name == 'None':
            return 0

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range

        for enemy_position in enemies_pos:

            if euclidean_distance(soldier_position, enemy_position) <= weapon_eff_range:
                count += 1
        return count

    def amount_enemies_out_of_effective_range(self, soldier, enemies, state):
        count = 0
        soldier_position = state.soldier_positions[soldier.id]
        weapon_eff_range = 0
        weapon_max_range = 0
        weapon_name = state.soldier_str_variables[soldier.id][2]

        if weapon_name == 'None':
            return 0

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range
                weapon_max_range = item.w_max_range

        for enemy_pos in enemies:
            if weapon_eff_range <= euclidean_distance(soldier_position, enemy_pos) <= weapon_max_range:
                count += 1
        return count

    """
    Weapon
    """
    def current_ammo_less_than_fire_rate(self, soldier):
        return soldier.equipped_weapon.current_ammo < soldier.equipped_weapon.fire_rate

    def change_weapon_variables(self, soldier, state):
        weapon_damage = 0
        fire_rate = 0
        w_eff_ran_p = 0
        w_max_ran_p = 0
        ef_ran = 0
        nef_ran = 0
        ammo_cap = 0

        precision = state.soldier_variables[soldier.id][11]
        weapon_name = state.soldier_str_variables[soldier.id][2]
        if weapon_name != 'None':
            current_ammo = state.soldier_weapons_current_ammo[soldier.id][weapon_name]
        else:
            current_ammo = 0

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_damage = item.damage
                fire_rate = item.fire_rate
                w_eff_ran_p = item.effective_range_precision
                w_max_ran_p = item.max_range_precision
                ef_ran = item.w_effective_range
                nef_ran = item.w_max_range
                ammo_cap = item.ammunition_capacity

        aff = 1
        if weapon_name != 'None':
            if weapon_name in soldier.w_affinities:
                aff = soldier.w_affinities[weapon_name]

        damage = weapon_damage * fire_rate * precision * aff

        damage_ef = damage * w_eff_ran_p
        damage_nef = damage * w_max_ran_p

        return damage_ef, damage_nef, fire_rate, current_ammo, ef_ran, nef_ran, ammo_cap

    """
    Survival
    """
    def concealment_value(self, soldier):
        return soldier.concealment

    def lost_health(self, soldier, state):
        return soldier.health - soldier.current_health

    def detect_objects(self, soldier, state):
        return soldier.detect_object(state.soldier_positions[soldier.id], self.map.terrain_matrix)

    def real_melee_attack(self, soldier, enemy_pos, state):
        result_state = state.copy_state()
        enemy = state.reverse_soldier_positions[enemy_pos]

        damage = soldier.melee_damage

        enemy.take_damage(damage)

        # NEW STATE
        change_en = [(10, state.soldier_variables[enemy.id][10] - damage), (11, enemy.precision)]
        en_tuple = new_changed_tuple(state.soldier_variables[enemy.id], change_en)
        result_state.soldier_variables[enemy.id] = en_tuple

        if state.soldier_variables[enemy.id][10] - damage <= 0:
            result_state.alive_soldiers[enemy.team] -= 1
            result_state.soldier_died[enemy.team][enemy.id] = True

        kill = False
        if state.soldier_variables[enemy.id][10] - damage <= 0:
            kill = True
            result_state.alive_soldiers[enemy.team] -= 1
            result_state.soldier_died[enemy.team][enemy.id] = True

        if kill:
            k = 1
        else:
            k = 0

        stats = [('kills', k)]

        return result_state, stats

    def real_shoot_enemy(self, soldier, enemy_pos, state):
        result_state = state.copy_state()

        pos1 = state.soldier_positions[soldier.id]
        enemy = state.reverse_soldier_positions[enemy_pos]

        # SHOOT
        damage, landed_shots = soldier.shoot(euclidean_distance(pos1, enemy_pos), self.weather.visibility_impairment, enemy.concealment)
        enemy.take_damage(damage)

        # NEW STATE
        change_en = [(10, state.soldier_variables[enemy.id][10] - damage), (11, enemy.precision)]
        change_sol = [(5, soldier.equipped_weapon.current_ammo)]

        sol_tuple = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        en_tuple = new_changed_tuple(state.soldier_variables[enemy.id], change_en)

        result_state.soldier_variables[soldier.id] = sol_tuple
        result_state.soldier_variables[enemy.id] = en_tuple
        result_state.soldier_weapons_current_ammo[soldier.id][state.soldier_str_variables[soldier.id][2]] = soldier.equipped_weapon.current_ammo

        kill = False
        if state.soldier_variables[enemy.id][10] - damage <= 0:
            kill = True
            result_state.alive_soldiers[enemy.team] -= 1
            result_state.soldier_died[enemy.team][enemy.id] = True

        # CALCULATE STATS
        # damage dealt
        d = damage
        # shots fired
        sf = min(state.soldier_variables[soldier.id][4], state.soldier_variables[soldier.id][5])
        if kill:
            k = 1
        else:
            k = 0

        stats = [('kills', k), ('shots', sf), ('shots landed', landed_shots), ('shots missed', sf - landed_shots)]

        return result_state, stats

    def real_move(self, soldier, position, state):

        if state.soldier_str_variables[soldier.id][0] == 'lying':
            return []

        result_state = state.copy_state()
        sol_position = state.soldier_positions[soldier.id]
        pos_matrix = soldier_pos_matrix(self.map, state)

        # STATE VALUES
        st_stance = state.soldier_str_variables[soldier.id][0]

        # SIMULATE MOVEMENT
        soldier.change_stance(st_stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)
        new_pos = soldier.move_to(sol_position, position, self.map.restriction_matrix, self.map.terrain_matrix, pos_matrix)

        new_concealment = soldier.concealment
        new_precision = soldier.precision
        new_next_object = soldier.next_to_object
        new_stance = soldier.stance

        # NEW STATE
        enemies_in_sight, enemies_in_eff_range, allies_in_eff_range, enemies_in_max_range = self._detect_allies_enemies(soldier, result_state)

        change_sol = [(0, enemies_in_sight), (1, allies_in_eff_range), (2, enemies_in_eff_range), (3, enemies_in_max_range), (9, new_concealment), (11, new_precision)]
        change_str_sol = [(0, new_stance), (1, new_next_object)]
        result_state.reverse_soldier_positions.pop(sol_position)

        result_state.soldier_positions[soldier.id] = new_pos
        result_state.reverse_soldier_positions[new_pos] = soldier
        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id], change_str_sol)

        stats = [('distance traveled', euclidean_distance(sol_position, new_pos))]

        return result_state, stats

    def real_change_stance(self, soldier, stance, state):

        result_state = state.copy_state()

        # STATE VALUE
        st_stance = state.soldier_str_variables[soldier.id][0]

        # SIMULATE ACTION
        soldier.change_stance(st_stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)
        soldier.change_stance(stance, state.soldier_positions[soldier.id], self.map.terrain_matrix)

        new_conceal = soldier.concealment
        new_precision = soldier.precision
        new_stance = soldier.stance
        new_next = soldier.next_to_object

        # NEW STATE
        change_sol = [(9, new_conceal), (11, new_precision)]
        change__str_sol = [(0, new_stance), (1, new_next)]

        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id],
                                                                           change__str_sol)

        return result_state

    def real_reload(self, soldier, state):

        result_state = state.copy_state()

        soldier.reload()

        # NEW STATE
        change_sol = [(5, soldier.equipped_weapon.current_ammo)]

        result_state.soldier_ammo_per_weapon[soldier.id][soldier.equipped_weapon.name] = soldier.weapon_ammo[soldier.equipped_weapon.name]
        result_state.soldier_weapons_current_ammo[soldier.id][soldier.equipped_weapon.name] = soldier.equipped_weapon.current_ammo
        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)

        return result_state

    def real_change_weapon(self, soldier, weapon_name, state):

        result_state = state.copy_state()

        soldier.change_weapon(weapon_name)

        # NEW STATE
        # damage_ef, damage_nef, fire_rate, current_ammo, ef_ran, nef_ran, ammo_cap
        new_variables = self.change_weapon_variables(soldier, state)

        position = state.soldier_positions[soldier.id]
        enemies_pos = soldier.detect_enemies(position, self.map.terrain_matrix, state)
        count_er = 0
        count_ner = 0
        for enemy_pos in enemies_pos:
            if euclidean_distance(position, enemy_pos) <= new_variables[4]:
                count_er += 1
                continue
            if euclidean_distance(position, enemy_pos) <= new_variables[5]:
                count_ner += 1

        change_sol = [(2, count_er),
                      (3, count_ner),
                      (4, new_variables[2]),
                      (5, new_variables[3]),
                      (6, new_variables[6]),
                      (7, new_variables[1]),
                      (8, new_variables[2])]

        result_state.soldier_variables[soldier.id] = new_changed_tuple(state.soldier_variables[soldier.id], change_sol)
        result_state.soldier_str_variables[soldier.id] = new_changed_tuple(state.soldier_str_variables[soldier.id], [(2, weapon_name)])
        result_state.soldier_weapons_current_ammo[soldier.id][weapon_name] = new_variables[3]

        return result_state

    def empty_action(self, state):

        return state
