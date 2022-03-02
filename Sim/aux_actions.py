from Sim.A_star.A_star import euclidean_distance


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

    # DETECTION
    def detect_enemies(self, soldier, terrain_map,  state=None):
        return soldier.detect_enemies(state.soldier_positions[soldier.id], terrain_map.terrain_matrix, state)

    def detect_enemies_withing_eff_range(self, soldier, terrain_map, state=None):
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

    def detect_enemies_withing_max_range(self, soldier, terrain_map, state=None):
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

    # get_position

def decorate_aux_actions(state):

    AuxActions.detect_allies = aux_action(state)(AuxActions.detect_allies)
    AuxActions.detect_enemies = aux_action(state)(AuxActions.detect_enemies)
    AuxActions.detect_enemies_withing_eff_range = aux_action(state)(AuxActions.detect_enemies_withing_eff_range)
    AuxActions.detect_enemies_withing_max_range = aux_action(state)(AuxActions.detect_enemies_withing_max_range)
