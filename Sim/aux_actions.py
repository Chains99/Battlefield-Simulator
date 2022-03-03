from Sim.A_star.A_star import euclidean_distance
from IA.Action_manager import soldier_pos_matrix

def add_state_to_args(args, state):
    args_list = list(args)
    new_args = []
    for arg in args_list:
        new_args.append(arg)
    new_args.append(state)

    return tuple(new_args)


# DECORATOR
def aux_action(state):

    def inner(function):

        def inner_args(*args, **kwargs):
            new_args = add_state_to_args(args, state)
            return function(*new_args)

        return inner_args

    return inner


class AuxActions:

    # AUX ACTIONS
    def detect_enemies(self, soldier, terrain_map,  state=None):
        enemies_pos = soldier.detect_enemies(state.soldier_positions[soldier.id], terrain_map.terrain_matrix, state)
        enemies = []
        for enemy_pos in enemies_pos:
            # add enemy instance
            enemies.append(state.reverse_soldier_positions[enemy_pos])
        return enemies

    def detect_enemies_within_eff_range(self, soldier, terrain_map, state=None):
        enemies_pos = soldier.detect_enemies(state.soldier_positions[soldier.id], terrain_map.terrain_matrix, state)
        soldier_position = state.soldier_positions[soldier.id]
        weapon_eff_range = 0
        weapon_name = state.soldier_str_variables[soldier.id][2]
        enemies_in_eff = []

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range
                weapon_max_range = item.w_max_range

        for enemy_pos in enemies_pos:
            if euclidean_distance(soldier_position, enemy_pos) <= weapon_eff_range:
                # add enemy instance
                enemies_in_eff.append(state.reverse_soldier_positions[enemy_pos])

        return enemies_in_eff

    def detect_enemies_within_max_range(self, soldier, terrain_map, state=None):
        enemies_pos = soldier.detect_enemies(state.soldier_positions[soldier.id], terrain_map.terrain_matrix, state)
        soldier_position = state.soldier_positions[soldier.id]
        weapon_eff_range = 0
        weapon_max_range = 0
        weapon_name = state.soldier_str_variables[soldier.id][2]
        enemies_in_max = []

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range
                weapon_max_range = item.w_max_range

        for enemy_pos in enemies_pos:
            if weapon_eff_range <= euclidean_distance(soldier_position, enemy_pos) <= weapon_max_range:
                # add enemy instance
                enemies_in_max.append(state.reverse_soldier_positions[enemy_pos])

        return enemies_in_max

    def detect_allies(self, soldier, terrain_map, state=None):
        return soldier.detect_allies(state.soldier_positions[soldier.id], terrain_map.terrain_matrix, state.reverse_soldier_positions)

    def get_position(self, soldier, state=None):
        if state is None:
            return [soldier.position[0], soldier.position[1]]
        pos = state.soldier_positions[soldier.id]
        return [pos[0], pos[1]]

    def shoot(self, soldier, enemy, state=None):
        sol_pos = state.soldier_positions[soldier.id]
        en_pos = state.soldier_positions[enemy.id]

        terrain_camouflage = soldier.terrain_map.terrain_matrix[en_pos[0]][en_pos[1]].camouflage
        damage, shot = soldier.shoot(euclidean_distance(sol_pos, en_pos), state.visibility_imp, min(state.soldier_variables[enemy.id][9] * terrain_camouflage, 0.95))

        enemy.take_damage(damage)

    def move(self, soldier, position, state=None):
        position = tuple(position)
        matrix = soldier_pos_matrix(soldier.terrain_map, state)
        sol_pos = state.soldier_positions[soldier.id]
        soldier.move_to(sol_pos, position, soldier.terrain_map.restriction_matrix, soldier.terrain_map.terrain_matrix, matrix)


def decorate_aux_actions(state):
    AuxActions.detect_allies = aux_action(state)(AuxActions.detect_allies)
    AuxActions.detect_enemies = aux_action(state)(AuxActions.detect_enemies)
    AuxActions.detect_enemies_within_eff_range = aux_action(state)(AuxActions.detect_enemies_within_eff_range)
    AuxActions.detect_enemies_within_max_range = aux_action(state)(AuxActions.detect_enemies_within_max_range)
    AuxActions.get_position = aux_action(state)(AuxActions.get_position)
    AuxActions.shoot = aux_action(state)(AuxActions.shoot)
    AuxActions.move = aux_action(state)(AuxActions.move)
